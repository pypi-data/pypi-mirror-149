import logging
import pandas as pd
import mxnet as mx
from mxnet.gluon.data import Dataset
from mxnet.gluon.contrib.estimator.batch_processor import BatchProcessor
from mxnet import ndarray, autograd
from mxnet import numpy as _mx_np
from mxnet.util import is_np_array
import boto3


class DownloadS3(object):
    def __init__(self, bucket, train_prefix, eval_prefix, parts_num=9999):
        self.bucket = bucket
        self.train_prefix = train_prefix
        self.eval_prefix = eval_prefix
        self.parts_num = parts_num
        self.data = None

    def download_train(self):
        keys = []
        df_list = []
        s3_client = boto3.client('s3', verify=False)

        resp = s3_client.list_objects_v2(Bucket=self.bucket, Prefix=self.train_prefix)
        for obj in resp['Contents']:
            if obj['Key'].endswith(".json"):
                keys.append(obj['Key'])

        for i, key in enumerate(keys):
            obj = s3_client.get_object(Bucket=self.bucket, Key=key)
            df = pd.read_json(obj['Body'], orient='columns', lines=True)
            df_list.append(df)
            if i > self.parts_num:
                break

        return pd.concat(df_list)

    def download_test(self):
        keys = []
        df_list = []
        s3_client = boto3.client('s3', verify=False)

        resp = s3_client.list_objects_v2(Bucket=self.bucket, Prefix=self.eval_prefix)
        for obj in resp['Contents']:
            if obj['Key'].endswith(".json"):
                keys.append(obj['Key'])

        for i, key in enumerate(keys):
            obj = s3_client.get_object(Bucket=self.bucket, Key=key)
            df = pd.read_json(obj['Body'], orient='columns', lines=True)
            df_list.append(df)
            if i > self.parts_num:
                break

        return pd.concat(df_list)


class DataIterLoaderTxT:
    def __init__(self, data_iter, seq_col, vl_col, context_cols):
        self.data_iter = data_iter
        self.seq_col = seq_col
        self.vl_col = vl_col
        self.context_cols = context_cols

    def __iter__(self):
        self.data_iter.reset()
        return self

    def __next__(self):
        batch = self.data_iter.__next__()
        data = batch.data
        label = batch.label[0]
        desc_list = list(x[0] for x in self.data_iter.provide_data)
        sequence_idx = desc_list.index(self.seq_col)
        vl_idx = desc_list.index(self.vl_col)
        context_idx = [desc_list.index(c) for c in self.context_cols]
        sequence_data = data[sequence_idx]
        valid_length = data[vl_idx]
        context_data = [data[i] for i in context_idx]
        return (sequence_data, valid_length, context_data), label

    def next(self):
        return self.__next__()


class BatchProcessorTxT(BatchProcessor):
    def __init__(self):
        pass

    def _get_data_and_label(self, batch, ctx, batch_axis=0):
        assert len(ctx) == 1, "Multiple CTX is not supported"
        array_fn = _mx_np.array if is_np_array() else ndarray.array

        data = [[array_fn(d, ctx[0]).as_in_context(ctx[0]) for d in batch[0]]]
        label = [array_fn(batch[1], ctx[0]).as_in_context(ctx[0])]
        # data = split_and_load(data, ctx_list=ctx, batch_axis=batch_axis)
        # label = split_and_load(label, ctx_list=ctx, batch_axis=batch_axis)
        return data, label

    def evaluate_batch(self, estimator,
                       val_batch,
                       batch_axis=0):
        data, label = self._get_data_and_label(val_batch, estimator.context, batch_axis)

        pred = [estimator.val_net(seq, vl, contexts, None) for seq, vl, contexts in data]
        loss = [estimator.val_loss(y_hat, y) for y_hat, y in zip(pred, label)]

        return data, label, pred, loss

    def fit_batch(self, estimator,
                  train_batch,
                  batch_axis=0):
        data, label = self._get_data_and_label(train_batch, estimator.context, batch_axis)

        with autograd.record():
            pred = [estimator.net(seq, vl, contexts, None) for seq, vl, contexts in data]
            loss = [estimator.loss(y_hat, y) for y_hat, y in zip(pred, label)]

        for l in loss:
            l.backward()

        return data, label, pred, loss


class DatasetTxT(Dataset):
    def __init__(self, data, seq_col, context_cols, vl_col, label_col):
        self.data = data
        self.seq_col = seq_col
        self.context_cols = context_cols
        self.vl_col = vl_col
        self.label_col = label_col

    def __getitem__(self, idx):
        seq = self.data.iloc[idx][self.seq_col]
        vl = self.data.iloc[idx][self.vl_col]
        contexts = self.data.iloc[idx][self.context_cols].tolist()
        label = self.data.iloc[idx][self.label_col]
        return (seq, vl, contexts), label

    def __len__(self):
        return len(self.data)


def evaluate_accuracy(data_iterator, model, ctx):
    acc = mx.metric.Accuracy()
    acc3 = mx.metric.TopKAccuracy(top_k=3)
    for i, ((sequence_data, valid_length, context_data), label) in enumerate(data_iterator):
        sequence = sequence_data.as_in_context(ctx)
        valid_length = valid_length.as_in_context(ctx)
        context = [d.as_in_context(ctx) for d in context_data]
        label = label.as_in_context(ctx)
        output = model(sequence, valid_length, context, None)
        # predictions = mx.nd.argmax(output, axis=1)
        # predictions3 = mx.nd.slice_axis(mx.nd.argsort(output, axis=1, is_ascend=False), axis=1, begin=0, end=3)
        acc.update(preds=output, labels=label)
        acc3.update(preds=output, labels=label)
    return float(acc.get()[1]), float(acc3.get()[1])


def load_s3_lookup(s3_bucket, s3_lookup, f_format="csv"):
    logger = logging.getLogger("load_s3")
    keys = []
    s3 = boto3.client('s3')
    list_obj = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_lookup)
    if list_obj["KeyCount"] > 1000:
        logger.error("Found more than 1000 keys and only read partial data")
    for content in list_obj["Contents"]:
        if content["Key"].endswith(f_format):
            keys.append(content["Key"])
    if len(keys) > 1:
        logger.error("Found more than 1 lookup %s" % f_format)
    obj = s3.get_object(Bucket=s3_bucket, Key=keys[0])
    logger.info("Load lookup table from %s" % keys[0])
    if f_format == "json":
        df = pd.read_json(obj["Body"], lines=True)
    elif f_format == "csv":
        df = pd.read_csv(obj["Body"])
    else:
        raise NotImplementedError()
    return df


def load_s3_offer_embed(s3_bucket, s3_key, mask_embed="zeros", save_local_path=None):
    s3 = boto3.resource('s3')
    obj = s3.Object(s3_bucket, s3_key)
    offer_embed_df = pd.read_json(obj.get()['Body'], lines=True)
    if save_local_path:
        offer_embed_df.to_json(save_local_path, orient="records", lines=True)
    if mask_embed == "zeros":
        embedding_weight = ndarray.array(
            pd.Series([[0] * 100], index=[-1]).append(offer_embed_df["embed_pca"]).reset_index(drop=True).tolist())
        return embedding_weight
    else:
        raise NotImplementedError()

