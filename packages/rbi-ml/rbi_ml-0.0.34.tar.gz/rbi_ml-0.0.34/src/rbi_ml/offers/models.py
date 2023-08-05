import math
import numpy as np
import mxnet as mx
from gluonnlp.data import UnigramCandidateSampler
from gluonnlp.model import ISDense
from gluonnlp.model.transformer import TransformerEncoder, TransformerEncoderCell
from mxnet import ndarray, gluon


class FrozenEmbedding(gluon.nn.Embedding):
    def __init__(self, frozen_weight, **kwargs):
        input_dim, output_dim = frozen_weight.shape
        super(FrozenEmbedding, self).__init__(input_dim=input_dim, output_dim=output_dim, **kwargs)
        self.frozen_weight = frozen_weight

    def initialize_frozen_weight(self, ctx=None, frozen_weight=None, freeze=True):
        self.initialize(force_reinit=True)
        if frozen_weight is not None:
            self.frozen_weight = frozen_weight
        self.weight.set_data(self.frozen_weight)
        if ctx is not None:
            self.weight.reset_ctx(ctx=ctx)
        if freeze:
            for param in self.collect_params().values():
                param.grad_req = "null"


class MeanMaxPooling(gluon.nn.HybridBlock):
    def __init__(self, axis=1, dropout=0.0, prefix=None, params=None, **kwargs):
        super().__init__(prefix=prefix, params=params)
        self.axis = axis
        self.dropout = gluon.nn.Dropout(rate=dropout)

    def hybrid_forward(self, F, inputs, valid_length=None):
        mean_out = F.mean(data=inputs, axis=self.axis) if valid_length is None \
            else F.sum(data=inputs, axis=self.axis) / valid_length
        max_out = F.max(data=inputs, axis=self.axis)
        outputs = F.concat(mean_out, max_out, dim=1)
        if self.dropout:
            outputs = self.dropout(outputs)
        #         outputs = F.LayerNorm(outputs)
        return outputs


class SequenceVAE(gluon.HybridBlock):
    def __init__(self, n_hidden=400, n_latent=100, n_layers=1, n_output=768+2048, batch_size=100,
                 act_type='relu', ctx=mx.cpu(), **kwargs):
        self.soft_zero = 1e-10
        self.n_latent = n_latent
        self.batch_size = batch_size
        self.model_ctx = ctx
        self.output = None
        self.mu = None
        # note to self: requring batch_size in model definition is sad, not sure how to deal with this otherwise though
        super(SequenceVAE, self).__init__(**kwargs)
        # self.use_aux_logits = use_aux_logits
        with self.name_scope():
            self.encoder = gluon.nn.HybridSequential(prefix='encoder')
            for i in range(n_layers):
                self.encoder.add(gluon.nn.Dense(n_hidden, activation=act_type))
            self.encoder.add(gluon.nn.Dense(n_latent * 2, activation=None))

            self.decoder = gluon.nn.HybridSequential(prefix='decoder')
            for i in range(n_layers):
                self.decoder.add(gluon.nn.Dense(n_hidden, activation=act_type))
            self.decoder.add(gluon.nn.Dense(n_output, activation='sigmoid'))

    def hybrid_forward(self, F, x):
        h = self.encoder(x)
        # print(h)
        mu_lv = F.split(h, axis=1, num_outputs=2)
        mu = mu_lv[0]
        lv = mu_lv[1]
        self.mu = mu
        # eps = F.random_normal(loc=0, scale=1, shape=mu.shape, ctx=model_ctx)
        # this would work fine only for nd (i.e. non-hybridized block)
        eps = F.random_normal(loc=0, scale=1, shape=(self.batch_size, self.n_latent),
                              ctx=self.model_ctx)
        z = mu + F.exp(0.5 * lv) * eps
        y = self.decoder(z)
        self.output = y

        KL = 0.5 * F.sum(1 + lv - mu * mu - F.exp(lv), axis=1)
        logloss = F.sum(x * F.log(y + self.soft_zero) + (1 - x) * F.log(1 - y + self.soft_zero), axis=1)
        loss = -logloss - KL

        return loss, z, y

    def initialize_frozen(self, param_path, batch_size, ctx):
        self.initialize(force_reinit=True)
        self.load_parameters(param_path, ctx=ctx)
        for param in self.collect_params().values():
            param.grad_req = "null"
        self.set_model_ctx(ctx=ctx)
        self.set_batch_size(batch_size=batch_size)

    def set_batch_size(self, batch_size):
        self.batch_size = batch_size

    def set_model_ctx(self, ctx):
        self.model_ctx = ctx


class SequenceTransformer(gluon.nn.HybridBlock):
    def __init__(self, num_items, item_embed, item_hidden_size, item_max_length, item_num_heads,
                 item_num_layers, item_transformer_dropout, item_pooling_dropout, cross_size, item_embedding_weight,
                 prefix=None, params=None, **kwargs):
        super().__init__(prefix=prefix, params=params)
        with self.name_scope():
            if item_embedding_weight is None:
                self.item_embedding = gluon.nn.Embedding(input_dim=num_items, output_dim=item_embed)
            else:
                self.item_embedding = FrozenEmbedding(frozen_weight=item_embedding_weight)
            self.item_encoder = TransformerEncoder(units=item_embed,
                                                   hidden_size=item_hidden_size,
                                                   num_heads=item_num_heads,
                                                   num_layers=item_num_layers,
                                                   max_length=item_max_length,
                                                   dropout=item_transformer_dropout)
            self.item_pooling_dp = MeanMaxPooling(dropout=item_pooling_dropout)
            self.dense = gluon.nn.Dense(cross_size)

    def hybrid_forward(self, F, input_item, item_valid_length=None, input_history=None):
        item_embed_out = self.item_embedding(input_item)
        if input_history is not None:
            history_embed_out = self.item_embedding(input_history)
            history_embed_avg = history_embed_out.mean(axis=1, keepdims=True)
            item_embed_out = F.concat(history_embed_avg, item_embed_out, dim=1)
            item_valid_length = F.broadcast_add(item_valid_length, F.ones_like(item_valid_length))
            # item_valid_length = mx.symbol.broadcast_add(item_valid_length, 1)
        item_encoding, item_att = self.item_encoder(inputs=item_embed_out, valid_length=item_valid_length)
        item_out = self.item_pooling_dp(item_encoding)
        item_out = self.dense(item_out)

        return item_out


class ContextTransformer(gluon.nn.HybridBlock):
    def __init__(self, context_dims, context_embed, context_hidden_size,
                 context_num_heads, context_transformer_dropout, context_pooling_dropout,
                 cross_size, prefix=None, params=None, **kwargs):
        super().__init__(prefix=prefix, params=params)
        self.context_dims = context_dims
        self.context_embed = context_embed
        self.cross_size = cross_size
        with self.name_scope():
            self.context_pooling_dp = MeanMaxPooling(dropout=context_pooling_dropout)
            self.context_encoder = TransformerEncoderCell(units=context_embed,
                                                          hidden_size=context_hidden_size,
                                                          num_heads=context_num_heads,
                                                          dropout=context_transformer_dropout
                                                          )
            self.dense = gluon.nn.Dense(self.cross_size)
            self.context_embeddings = gluon.nn.HybridSequential()
            for i, context_dim in enumerate(self.context_dims):
                self.context_embeddings.add(gluon.nn.Embedding(self.context_dims[i], self.context_embed))

    def hybrid_forward(self, F, input_context_list):
        context_embed = [self.context_embeddings[i](input_context) for i, input_context in enumerate(input_context_list)]
        context_input = []
        for i in context_embed:
            context_input.append(F.expand_dims(i, axis=1))
        context_embedding = F.concat(*context_input, dim=1)
        context_encoding, context_att = self.context_encoder(context_embedding)
        context_out = self.context_pooling_dp(context_encoding)
        context_out = self.dense(context_out)

        return context_out


class TxT(gluon.nn.HybridBlock):
    def __init__(self,
                 num_items,
                 context_dims,
                 item_embed=200,
                 context_embed=100,
                 item_hidden_size=512,
                 item_max_length=5,
                 item_num_heads=4,
                 item_num_layers=2,
                 item_transformer_dropout=0.0,
                 item_pooling_dropout=0.0,
                 context_hidden_size=512,
                 context_num_heads=2,
                 context_transformer_dropout=0.0,
                 context_pooling_dropout=0.0,
                 act_type="gelu",
                 cross_size=200,
                 item_embedding_weight=None,
                 prefix=None,
                 params=None,
                 **kwargs):
        super(TxT, self).__init__(**kwargs)
        self.act_type = act_type
        with self.name_scope():
            self.sequence_transformer = SequenceTransformer(
                num_items=num_items,
                item_embed=item_embed,
                item_hidden_size=item_hidden_size,
                item_max_length=item_max_length,
                item_num_heads=item_num_heads,
                item_num_layers=item_num_layers,
                item_transformer_dropout=item_transformer_dropout,
                item_pooling_dropout=item_pooling_dropout,
                cross_size=cross_size,
                item_embedding_weight=item_embedding_weight,
                prefix=prefix,
                params=params,
            )
            self.context_transformer = ContextTransformer(
                context_dims=context_dims,
                context_embed=context_embed,
                context_hidden_size=context_hidden_size,
                context_num_heads=context_num_heads,
                context_transformer_dropout=context_transformer_dropout,
                context_pooling_dropout=context_pooling_dropout,
                cross_size=cross_size,
                prefix=prefix,
                params=params,
            )
            self.dense1 = gluon.nn.Dense(units=num_items//2)
            if act_type == "relu":
                self.act = gluon.nn.Activation(activation="relu")
            elif act_type == "gelu":
                self.act = gluon.nn.GELU()
            elif act_type == "leakyRelu":
                self.act = gluon.nn.LeakyReLU(alpha=0.2)
            else:
                raise NotImplementedError
            self.dense2 = gluon.nn.Dense(units=num_items, activation=None)

    def hybrid_forward(self, F, input_item, item_valid_length, input_context_list, input_history=None):
        item_outs = self.sequence_transformer(input_item, item_valid_length, input_history)
        context_outs = self.context_transformer(input_context_list)

        outs = F.broadcast_mul(item_outs, context_outs)
        outs = self.dense1(outs)
        outs = self.act(outs)
        outs = self.dense2(outs)

        return outs
