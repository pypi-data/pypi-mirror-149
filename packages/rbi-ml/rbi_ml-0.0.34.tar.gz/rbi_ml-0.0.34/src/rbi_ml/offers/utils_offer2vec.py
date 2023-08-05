import time
import math
import logging
import itertools
import functools
from contextlib import contextmanager
import numpy as np
import gluonnlp as nlp
import mxnet as mx


logger = logging.getLogger("offer_encoder_offer2vec")


# Help functions - utils

def get_context(args):
    if args.gpu is None or args.gpu == '':
        context = [mx.cpu()]
    elif isinstance(args.gpu, int):
        context = [mx.gpu(args.gpu)]
    else:
        context = [mx.gpu(int(i)) for i in args.gpu]
    return context


@contextmanager
def print_time(task):
    start_time = time.time()
    logging.info('Starting to %s', task)
    yield
    logging.info('Finished to {} in {:.2f} seconds'.format(
        task,
        time.time() - start_time))


# Helper functions - data

def preprocess_dataset(data, vocab_len=None, min_freq=1, max_vocab_size=None):
    with print_time('count and construct vocabulary'):
        counter = nlp.data.count_tokens(itertools.chain.from_iterable(data))
        if vocab_len:
            counter.update(range(vocab_len))
            logger.info("Build vocab with indexed data of length %d" % vocab_len)
            vocab = nlp.Vocab(
                counter,
                token_to_idx={x: x for x in counter.keys()},
                unknown_token=None,
                mask_token=None,
                padding_token=0,
                bos_token=None,
                eos_token=None,
                min_freq=min_freq,
                max_size=max_vocab_size
            )
        else:
            logger.info("Build vocab with unindexed data")
            vocab = nlp.Vocab(
                counter,
                unknown_token=None,
                mask_token=None,
                padding_token=0,
                bos_token=None,
                eos_token=None,
                min_freq=min_freq,
                max_size=max_vocab_size
            )
        idx_to_counts = [counter[w] for w in vocab.idx_to_token]

    def code(sentence):
        return [vocab[token] for token in sentence if token in vocab]

    with print_time('code data'):
        data = data.transform(code, lazy=False)
    data = nlp.data.SimpleDataStream([data])
    return data, vocab, idx_to_counts


def transform_data_word2vec(data, vocab, idx_to_counts, cbow, batch_size,
                            window_size, frequent_token_subsampling=1E-4,
                            dtype='float32', index_dtype='int64'):
    """Transform a DataStream of coded DataSets to a DataStream of batches.

    Parameters
    ----------
    data : gluonnlp.data.DataStream
        DataStream where each sample is a valid input to
        gluonnlp.data.EmbeddingCenterContextBatchify.
    vocab : gluonnlp.Vocab
        Vocabulary containing all tokens whose indices occur in data.
    idx_to_counts : list of int
        List of integers such that idx_to_counts[idx] represents the count of
        vocab.idx_to_token[idx] in the underlying dataset. The count
        information is used to subsample frequent words in the dataset.
        Each token is independently dropped with probability 1 - sqrt(t /
        (count / sum_counts)) where t is the hyperparameter
        frequent_token_subsampling.
    cbow : boolean
        If True, use CBOW. Otherwise, use SkipGram
    batch_size : int
        The returned data stream iterates over batches of batch_size.
    window_size : int
        The context window size for
        gluonnlp.data.EmbeddingCenterContextBatchify.
    frequent_token_subsampling : float
        Hyperparameter for subsampling. See idx_to_counts above for more
        information.
    dtype : str or np.dtype, default 'float32'
        Data type of data array.
    index_dtype : str or np.dtype, default 'int64'
        Data type of index arrays.

    Returns
    -------
    gluonnlp.data.DataStream
        Stream over batches.
    """

    sum_counts = float(sum(idx_to_counts))
    idx_to_pdiscard = [
        1 - math.sqrt(frequent_token_subsampling / (count / sum_counts))
        for count in idx_to_counts]

    def subsample(shard):
        return [[
            t for t, r in zip(sentence,
                              np.random.uniform(0, 1, size=len(sentence)))
            if r > idx_to_pdiscard[t]] for sentence in shard]

    data = data.transform(subsample)

    batchify = nlp.data.batchify.EmbeddingCenterContextBatchify(
        batch_size=batch_size, window_size=window_size, cbow=cbow,
        weight_dtype=dtype, index_dtype=index_dtype, shuffle=True)
    data = data.transform(batchify)
    data = UnchainStream(data)

    if cbow:
        batchify_fn = cbow_batch
    else:
        batchify_fn = skipgram_batch
    batchify_fn = functools.partial(batchify_fn, num_tokens=len(vocab),
                                    dtype=dtype, index_dtype=index_dtype)

    return data, batchify_fn,


class UnchainStream(nlp.data.DataStream):
    def __init__(self, iterable):
        self._stream = iterable

    def __iter__(self):
        return iter(itertools.chain.from_iterable(self._stream))


def cbow_batch(centers, contexts, num_tokens, dtype, index_dtype):
    """Create a batch for CBOW training objective."""
    contexts_data, contexts_row, contexts_col = contexts
    centers = mx.nd.array(centers, dtype=index_dtype)
    contexts = mx.nd.sparse.csr_matrix(
        (contexts_data, (contexts_row, contexts_col)),
        dtype=dtype, shape=(len(centers), num_tokens))  # yapf: disable
    return centers, contexts


def skipgram_batch(centers, contexts, num_tokens, dtype, index_dtype):
    """Create a batch for SG training objective."""
    contexts = mx.nd.array(contexts[2], dtype=index_dtype)
    indptr = mx.nd.arange(len(centers) + 1)
    centers = mx.nd.array(centers, dtype=index_dtype)
    centers_csr = mx.nd.sparse.csr_matrix(
        (mx.nd.ones(centers.shape), centers, indptr), dtype=dtype,
        shape=(len(centers), num_tokens))
    return centers_csr, contexts, centers


# Helper functions - model

class Net(mx.gluon.HybridBlock):
    """Base class for word2vec and fastText SkipGram and CBOW networks.

    Parameters
    ----------
    token_to_idx : dict
        token_to_idx mapping of the vocabulary that this model is to be trained
        with. token_to_idx is used for __getitem__ and __contains__. For
        len(token_to_idx) is used during initialization to obtain the input_dim
        of the embedding matrix.
    output_dim : int
        Dimension of the dense embedding.
    batch_size : int
        Batchsize this model will be trained with. TODO temporary until
        random_like ops are supported
    negatives_weights : mxnet.nd.NDArray
        Weights for UnigramCandidateSampler for sampling negatives.
    smoothing : float, default 0.75
        Smoothing factor applied to negatives_weights. Final weights are
        mxnet.nd.power(negative_weights, smoothing).
    num_negatives : int, default 5
        Number of negatives to sample for each real sample.
    sparse_grad : bool, default True
        Specifies mxnet.gluon.nn.Embedding sparse_grad argument.
    dtype : str, default 'float32'
        dtype argument passed to gluon.nn.Embedding

    """

    # pylint: disable=abstract-method
    def __init__(self, token_to_idx, output_dim, negatives_weights,
                 subword_function=None, num_negatives=5, smoothing=0.75,
                 sparse_grad=True, dtype='float32', **kwargs):
        super(Net, self).__init__(**kwargs)

        self._kwargs = dict(
            input_dim=len(token_to_idx), output_dim=output_dim, dtype=dtype,
            sparse_grad=sparse_grad, num_negatives=num_negatives)

        with self.name_scope():
            if subword_function is not None:
                self.embedding = nlp.model.train.FasttextEmbeddingModel(
                    token_to_idx=token_to_idx,
                    subword_function=subword_function,
                    output_dim=output_dim,
                    weight_initializer=mx.init.Uniform(scale=1 / output_dim),
                    sparse_grad=sparse_grad,
                )
            else:
                self.embedding = nlp.model.train.CSREmbeddingModel(
                    token_to_idx=token_to_idx,
                    output_dim=output_dim,
                    weight_initializer=mx.init.Uniform(scale=1 / output_dim),
                    sparse_grad=sparse_grad,
                )
            self.embedding_out = mx.gluon.nn.Embedding(
                len(token_to_idx), output_dim=output_dim,
                weight_initializer=mx.init.Zero(), sparse_grad=sparse_grad,
                dtype=dtype)

            self.negatives_sampler = nlp.data.UnigramCandidateSampler(
                weights=negatives_weights**smoothing, dtype='int64')

    def __getitem__(self, tokens):
        return self.embedding[tokens]

    def hybrid_forward(self, F, x, *args, **kwargs):
        raise NotImplementedError()


class SG(Net):
    """SkipGram network"""

    # pylint: disable=arguments-differ
    def hybrid_forward(self, F, center, context, center_words):
        """SkipGram forward pass.

        Parameters
        ----------
        center : mxnet.nd.NDArray or mxnet.sym.Symbol
            Sparse CSR array of word / subword indices of shape (batch_size,
            len(token_to_idx) + num_subwords). Embedding for center words are
            computed via F.sparse.dot between the CSR center array and the
            weight matrix.
        context : mxnet.nd.NDArray or mxnet.sym.Symbol
            Dense array of context words of shape (batch_size, ). Also used for
            row-wise independently masking negatives equal to one of context.
        center_words : mxnet.nd.NDArray or mxnet.sym.Symbol
            Dense array of center words of shape (batch_size, ). Only used for
            row-wise independently masking negatives equal to one of
            center_words.
        """

        # negatives sampling
        negatives = []
        mask = []
        for _ in range(self._kwargs['num_negatives']):
            negatives.append(self.negatives_sampler(center_words))
            mask_ = negatives[-1] != center_words
            mask_ = F.stack(mask_, (negatives[-1] != context))
            mask.append(mask_.min(axis=0))

        negatives = F.stack(*negatives, axis=1)
        mask = F.stack(*mask, axis=1).astype(np.float32)

        # center - context pairs
        emb_center = self.embedding(center).expand_dims(1)
        emb_context = self.embedding_out(context).expand_dims(2)
        pred_pos = F.batch_dot(emb_center, emb_context).squeeze()
        loss_pos = (F.relu(pred_pos) - pred_pos + F.Activation(
            -F.abs(pred_pos), act_type='softrelu')) / (mask.sum(axis=1) + 1)

        # center - negatives pairs
        emb_negatives = self.embedding_out(negatives).reshape(
            (-1, self._kwargs['num_negatives'],
             self._kwargs['output_dim'])).swapaxes(1, 2)
        pred_neg = F.batch_dot(emb_center, emb_negatives).squeeze()
        mask = mask.reshape((-1, self._kwargs['num_negatives']))
        loss_neg = (F.relu(pred_neg) + F.Activation(
            -F.abs(pred_neg), act_type='softrelu')) * mask
        loss_neg = loss_neg.sum(axis=1) / (mask.sum(axis=1) + 1)

        return loss_pos + loss_neg


class CBOW(Net):
    """CBOW network"""

    # pylint: disable=arguments-differ
    def hybrid_forward(self, F, center, context):
        """CBOW forward pass.

        Parameters
        ----------
        center : mxnet.nd.NDArray or mxnet.sym.Symbol
            Dense array of center words of shape (batch_size, ).
        context : mxnet.nd.NDArray or mxnet.sym.Symbol
            Sparse CSR array of word / subword indices of shape (batch_size,
            len(vocab) + num_subwords). Embedding for context words are
            computed via F.sparse.dot between the CSR center array and the
            weight matrix.

        """
        # negatives sampling
        negatives = []
        mask = []
        for _ in range(self._kwargs['num_negatives']):
            negatives.append(self.negatives_sampler(center))
            mask.append(negatives[-1] != center)

        negatives = F.stack(*negatives, axis=1)
        mask = F.stack(*mask, axis=1).astype(np.float32)

        # context - center samples
        emb_context = self.embedding(context).expand_dims(1)
        emb_center = self.embedding_out(center).expand_dims(2)
        pred_pos = F.batch_dot(emb_context, emb_center).squeeze()
        loss_pos = (F.relu(pred_pos) - pred_pos + F.Activation(
            -F.abs(pred_pos), act_type='softrelu')) / (mask.sum(axis=1) + 1)

        # context - negatives samples
        emb_negatives = self.embedding_out(negatives).reshape(
            (-1, self._kwargs['num_negatives'],
             self._kwargs['output_dim'])).swapaxes(1, 2)
        pred_neg = F.batch_dot(emb_context, emb_negatives).squeeze()
        mask = mask.reshape((-1, self._kwargs['num_negatives']))
        loss_neg = (F.relu(pred_neg) + F.Activation(
            -F.abs(pred_neg), act_type='softrelu')) * mask
        loss_neg = loss_neg.sum(axis=1) / (mask.sum(axis=1) + 1)

        return loss_pos + loss_neg


# Helper functions - train and eval

def norm_vecs_by_row(x):
    return x / (mx.nd.sum(x * x, axis=1) + 1e-10).sqrt().reshape((-1, 1))


def get_k_closest_offers(vocab, embedding, k, offer, offer_to_name):
    offer_vec = norm_vecs_by_row(embedding[[offer]])
    vocab_vecs = norm_vecs_by_row(embedding[vocab.idx_to_token])
    dot_prod = mx.nd.dot(vocab_vecs, offer_vec.T)
    indices = mx.nd.topk(
        dot_prod.reshape((len(vocab.idx_to_token), )),
        k=k+1,
        ret_typ='indices')
    indices = [int(i.asscalar()) for i in indices]
    result = [offer_to_name[vocab.idx_to_token[i]] for i in indices[1:]]
    logger.info('closest tokens to "%s":\n\t%s' % (offer_to_name[offer], "\n\t".join(result)))


def train_embedding(vocab, batches, embedding, trainer, ctx, num_epochs, log_interval, offer_to_name, model_save_path):
    for epoch in range(1, num_epochs + 1):
        start_time = time.time()
        l_avg = 0
        log_wc = 0

        logger.info('Beginning epoch %d and resampling data.' % epoch)
        for i, batch in enumerate(batches):
            batch = [array.as_in_context(ctx) for array in batch]
            with mx.autograd.record():
                loss = embedding(*batch)
            loss.backward()
            trainer.step(1)

            l_avg += loss.mean()
            log_wc += loss.shape[0]
            if i % log_interval == 0:
                # mx.nd.waitall()
                wps = log_wc / (time.time() - start_time)
                l_avg = l_avg.asscalar() / log_interval
                logger.info('epoch %d, iteration %d, loss %.2f, throughput=%.2fK wps' % (epoch, i, l_avg, wps / 1000))
                start_time = time.time()
                log_wc = 0
                l_avg = 0

        embedding.export(model_save_path, epoch + 1)
        logger.info("model has been saved")
        get_k_closest_offers(vocab, embedding, 10, 46, offer_to_name)  # 46: $8.99 Whopper Meal for Two
    return None


# Main functions

def get_offer2vec_features(offer_pool_all, offer_bag_data, model_save_path, ctx, mode, embedding_size=100,
                           batch_size=4096, window_size=3, frequent_token_subsampling=1E-1, num_negatives=5,
                           learning_rate=0.05, num_epochs=1, log_interval=500, **kwargs):
    assert mode in ["cbow", "CBOW", "sg", "SG"], "mode should be either 'CBOW' or 'SG'"
    data_raw = mx.gluon.data.dataset.SimpleDataset(offer_bag_data)
    offer_count = len(offer_pool_all)
    offer_to_name = {
        k: v["offer_name"]
        for k, v in offer_pool_all[["offer_name", "offer_idx"]].set_index("offer_idx").to_dict(orient="index").items()
    }
    is_cbow = True if mode in ["cbow", "CBOW"] else False

    # before indexing
    log_string = f"# sentences (user count): {len(data_raw)}\n"
    for i, sentence in enumerate(data_raw):
        log_string += f"\t# tokens: {len(sentence)} {sentence[:10]}\n"
        if i > 2:
            break
    logger.info(log_string)

    # build vocab and index
    data_idx, vocab, idx_to_counts = preprocess_dataset(
        data=data_raw,
        vocab_len=offer_count,
        min_freq=1,
        max_vocab_size=None
    )
    assert all([k == v for k, v in vocab.token_to_idx.items()]), "offer_idx != idx"

    # after indexing
    log_string = f"# sentences (user count): {len(data_raw)}\n"
    for sentences in data_idx:
        for i, sentence in enumerate(sentences):
            log_string += f"\t# tokens: {len(sentence)} {sentence[:10]}\n"
            if i > 2:
                break
    logger.info(log_string)

    # subsample and generate context-center pairs
    data, batchify_fn = transform_data_word2vec(
        data=data_idx,
        vocab=vocab,
        idx_to_counts=idx_to_counts,
        cbow=is_cbow,
        batch_size=batch_size,
        window_size=window_size,
        frequent_token_subsampling=frequent_token_subsampling,
    )

    # for i, d in enumerate(data):
    #     print(d)
    #     break

    # batchify
    batches = data.transform(batchify_fn)

    # for i, d in enumerate(batches):
    #     print(d)
    #     break

    negatives_weights = mx.nd.array(idx_to_counts)
    if is_cbow:
        embedding = CBOW(
            token_to_idx=vocab.token_to_idx,
            output_dim=embedding_size,
            negatives_weights=negatives_weights,
            subword_function=None,
            num_negatives=num_negatives,
            smoothing=0.75,
            sparse_grad=True,
            dtype="float32",
        )
    else:
        embedding = SG(
            token_to_idx=vocab.token_to_idx,
            output_dim=embedding_size,
            negatives_weights=negatives_weights,
            subword_function=None,
            num_negatives=num_negatives,
            smoothing=0.75,
            sparse_grad=True,
            dtype="float32",
        )
    embedding.initialize(ctx=ctx)
    embedding.hybridize()
    trainer = mx.gluon.Trainer(embedding.collect_params(), 'adagrad', dict(learning_rate=learning_rate))
    logger.info(embedding)

    train_embedding(
        vocab=vocab,
        batches=batches,
        embedding=embedding,
        trainer=trainer,
        ctx=ctx,
        num_epochs=num_epochs,
        log_interval=log_interval,
        offer_to_name=offer_to_name,
        model_save_path=model_save_path,
    )
    offer2vec_features = embedding[vocab.idx_to_token].asnumpy()

    return offer2vec_features

