import os
import time
import json
import math
import numpy as np
import pandas as pd
import boto3
import torch
import wandb
from torch.utils.data import Dataset
import mlflow
import pytorch_lightning as pl
from pytorch_lightning import LightningModule
from .callbacks_base import AttnVisCallbackBase, TensorboardCallbackBase
from ..models.txt import TxT


class TxTTensorboardCallback(TensorboardCallbackBase):
    def __init__(self, tensorboard_logger):
        super().__init__(tensorboard_logger)

    def update_metrics_scalar(self, trainer, pl_module, phase):
        pass


class TxTContextAttnVisCallback(AttnVisCallbackBase):
    def __init__(self, transformer_prefix, cols, sample_inputs, device):
        super().__init__(transformer_prefix, cols, sample_inputs, device)

    def get_attn_weights(self, pl_module):
        ctx_embedding_layers = pl_module.txt.context_transformer.ctx_embedding
        attn_layer = pl_module.txt.context_transformer.ctx_encoder.layers[0].self_attn
        ctx_embedding_list = [ctx_embedding_layers[i](input_ctx.to(self.device)).unsqueeze(1)
                              for i, input_ctx in enumerate(self.sample_inputs)]
        ctx_out = torch.cat(ctx_embedding_list, dim=1)
        _, attn_weight = attn_layer(ctx_out, ctx_out, ctx_out, need_weights=True)
        avg_attn_weight = attn_weight.mean(0).mean(0).detach().tolist()
        return avg_attn_weight


class TxTSequenceAttnVisCallback(AttnVisCallbackBase):
    def __init__(self, transformer_prefix, cols, sample_inputs, device):
        super().__init__(transformer_prefix, cols, sample_inputs, device)

    def get_attn_weights(self, pl_module):
        seq_in = self.sample_inputs[0].to(self.device)
        vl_in = self.sample_inputs[1].to(self.device)
        sequence_transformer_layer = pl_module.txt.sequence_transformer
        attn_layer = pl_module.txt.sequence_transformer.seq_encoder.layers[0].self_attn
        seq_out = sequence_transformer_layer.seq_embedding(seq_in.long())
        seq_out = seq_out * math.sqrt(sequence_transformer_layer.seq_embed_size)
        seq_out = sequence_transformer_layer.pos_encoder(seq_out)
        mask = sequence_transformer_layer.create_key_padding_mask(seq_in=seq_in, valid_length=vl_in)
        _, attn_weight = attn_layer(seq_out, seq_out, seq_out, key_padding_mask=mask, need_weights=True)
        avg_attn_weight = attn_weight.mean(0).mean(0).detach().tolist()
        return avg_attn_weight


class TxTWandbArtifactCallback(pl.callbacks.Callback):
    def __init__(self, wandb_run, lookup_output_dir, torch_model_params, pl_model_params, model_dir):
        self.wandb_run = wandb_run
        self.model_dir = model_dir
        self.lookup_output_dir = lookup_output_dir
        self.torch_model_params = torch_model_params
        pl_model_params["loss"] = str(pl_model_params["loss"])
        pl_model_params["optimizer"] = str(pl_model_params["optimizer"])
        pl_model_params["txt_kwargs"]["ctx_nums"] = [
            int(i) for i in pl_model_params["txt_kwargs"]["ctx_nums"]
        ]
        self.pl_model_params = pl_model_params

    def on_train_start(self, trainer, pl_module):
        # lookup files
        lookup_artifact = wandb.Artifact("lookup_csv", type="lookup_tables")
        lookup_artifact.add_dir(self.lookup_output_dir)
        self.wandb_run.log_artifact(lookup_artifact, aliases=[self.wandb_run.name])
        # torch model params
        torch_model_params_path = os.path.join(self.model_dir, "torch_model_params.json")
        with open(torch_model_params_path, "w") as f:
            json.dump(self.torch_model_params, f)
        torch_params_artifact = wandb.Artifact("torch_params", type="params")
        torch_params_artifact.add_file(torch_model_params_path)
        self.wandb_run.log_artifact(torch_params_artifact, aliases=[self.wandb_run.name])
        # pl model params
        pl_model_params_path = os.path.join(self.model_dir, "pl_model_params.json")
        with open(pl_model_params_path, "w") as f:
            json.dump(self.pl_model_params, f)
        pl_params_artifact = wandb.Artifact("pl_params", type="params")
        pl_params_artifact.add_file(pl_model_params_path)
        self.wandb_run.log_artifact(pl_params_artifact, aliases=[self.wandb_run.name])

    def on_train_epoch_end(self, trainer, pl_module):
        # torch model
        model_path = os.path.join(self.model_dir, f"model.pt")
        torch.save(pl_module.txt.state_dict(), model_path)
        torch_model_artifact = wandb.Artifact(f"torch_model_epoch_{pl_module.current_epoch}", type="model")
        torch_model_artifact.add_file(model_path)
        self.wandb_run.log_artifact(torch_model_artifact, aliases=[self.wandb_run.name])

    def on_train_end(self, trainer, pl_module):
        # pl model
        model_path = os.path.join(self.model_dir, f"model.pt")
        torch.save(pl_module.state_dict(), model_path)
        pl_model_artifact = wandb.Artifact(f"pl_model_epoch_{pl_module.current_epoch}", type="model")
        pl_model_artifact.add_file(model_path)
        self.wandb_run.log_artifact(pl_model_artifact, aliases=[self.wandb_run.name])


class TxTOrderDataset(Dataset):
    """
    If from_s3 is True, will read data from s3. s3_bucket, s3_prefix_data and s3_prefix_lookups are required.
    Otherwise will read local data. local_data_data_dir and local_lookup_dirs are required.
    """
    def __init__(self, ctx_cols, seq_col, vl_col, label_col,
                 from_s3=True, local_data_dir=None, local_lookup_dirs=None,
                 s3_bucket=None, s3_prefix_data=None, s3_prefix_lookups=None,
                 parts_num=9999, data_file_format="json", lookup_file_format="json"):
        self.ctx_cols = ctx_cols
        self.seq_col = seq_col
        self.vl_col = vl_col
        self.label_col = label_col
        self.local_data_dir = local_data_dir
        self.local_lookup_dirs = local_lookup_dirs
        self.s3_bucket = s3_bucket
        self.s3_prefix_data = s3_prefix_data
        self.s3_prefix_lookups = s3_prefix_lookups
        self.parts_num = parts_num
        self.data_file_format = data_file_format
        self.lookup_file_format = lookup_file_format
        # load data
        self.ctx_np = []
        self.seq_np = []
        self.vl_np = []
        self.label_np = []
        self.lookups = {}
        if from_s3:
            assert s3_bucket and s3_prefix_data and s3_prefix_lookups
            self._load_lookups_from_s3()
            self._load_data_from_s3()
        else:
            assert local_data_dir, local_lookup_dirs
            self._load_lookups_from_local()
            self._load_data_from_local()

        # convert dataframe to numpy
        self.ctx_np = np.concatenate(self.ctx_np, axis=0)
        self.seq_np = np.concatenate(self.seq_np, axis=0)
        self.vl_np = np.concatenate(self.vl_np, axis=0)
        self.label_np = np.concatenate(self.label_np, axis=0)
        self.len_data = len(self.ctx_np)

    @staticmethod
    def _read_df(path, file_format):
        if file_format == "json":
            return pd.read_json(path, lines=True)
        elif file_format == "csv":
            return pd.read_csv(path)

    def _append_np_from_df(self, df):
        self.ctx_np.append(np.array(df[self.ctx_cols]))
        self.seq_np.append(np.array(df[self.seq_col].to_list()))
        self.vl_np.append(np.array(df[self.vl_col]))
        self.label_np.append(np.array(df[self.label_col].astype(float)))

    def _load_data_from_s3(self):
        keys = []
        s3_client = boto3.client('s3')
        resp = s3_client.list_objects_v2(Bucket=self.s3_bucket, Prefix=self.s3_prefix_data)
        for obj in resp['Contents']:
            if obj['Key'].endswith(self.data_file_format):
                keys.append(obj['Key'])
        for i, key in enumerate(keys):
            obj = s3_client.get_object(Bucket=self.s3_bucket, Key=key)
            df = self._read_df(obj['Body'], file_format=self.data_file_format)
            self._append_np_from_df(df)
            if i > self.parts_num:
                break

    def _load_data_from_local(self):
        f_paths = [
            os.path.join(self.local_data_dir, f_name)
            for f_name in os.listdir(self.local_data_dir)
            if f_name.endswith(self.data_file_format)
        ]
        for i, f_path in enumerate(f_paths):
            df = self._read_df(f_path, self.data_file_format)
            self._append_np_from_df(df)
            if i > self.parts_num:
                break

    def _load_lookups_from_s3(self):
        for s3_prefix in self.s3_prefix_lookups:
            lookup_name = os.path.split(s3_prefix[:-1])[1] if s3_prefix.endswith("/") else os.path.split(s3_prefix)[1]
            keys = []
            s3_client = boto3.client('s3')
            resp = s3_client.list_objects_v2(Bucket=self.s3_bucket, Prefix=s3_prefix)
            for obj in resp['Contents']:
                if obj['Key'].endswith(self.lookup_file_format):
                    keys.append(obj['Key'])
            assert len(keys) == 1, "should only have one lookup table per folder"
            obj = s3_client.get_object(Bucket=self.s3_bucket, Key=keys[0])
            df = self._read_df(obj['Body'], file_format=self.lookup_file_format)

            self.lookups[lookup_name] = df

    def _load_lookups_from_local(self):
        for local_dir in self.local_lookup_dirs:
            lookup_name = os.path.split(local_dir[:-1])[1] if local_dir.endswith("/") else os.path.split(local_dir)[1]
            local_paths = [
                file_name for file_name in os.listdir(local_dir)
                if file_name.endswith(self.lookup_file_format)
            ]
            assert len(local_paths) == 1, "should only have one lookup table per folder"
            df = self._read_df(os.path.join(local_dir, local_paths[0]), file_format=self.lookup_file_format)
            self.lookups[lookup_name] = df

    def __len__(self):
        return self.len_data

    def __getitem__(self, idx):
        ctx = [i for i in self.ctx_np[idx]]
        seq = torch.tensor(self.seq_np[idx])
        vl = self.vl_np[idx]
        label = self.label_np[idx]
        data = (ctx, seq, vl)
        return data, label

    def get_feature_num(self, col):
        if col == self.ctx_cols[0]:
            return int(self.ctx_np[:, 0].astype(int).max() + 1)
        elif col == self.ctx_cols[1]:
            return int(self.ctx_np[:, 1].astype(int).max() + 1)
        elif col == self.ctx_cols[2]:
            return int(self.ctx_np[:, 2].astype(int).max() + 1)
        elif col == self.seq_col:
            return int(self.seq_np.reshape(-1).max()) + 1
        # elif data_col.dtype == "object":
        #     return int(np.array(data_col.to_list()).max()) + 1
        else:
            raise NotImplementedError()

    def export_lookups(self, local_dir, file_format):
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        for lookup_name, lookup_df in self.lookups.items():
            output_path = os.path.join(local_dir, f"{lookup_name}.{file_format}")
            if file_format == "json":
                lookup_df.to_json(output_path)
            elif file_format == "csv":
                lookup_df.to_csv(output_path, index=False)
            else:
                raise NotImplementedError()

class KRTxTOrderDataset(TxTOrderDataset):
    """ OrderDataset class for KR dataset """
    def __init__(self, ctx_cols, seq_col, vl_col, history_col, label_col,
                 is_train=True, from_s3=True, local_data_dir=None, local_lookup_dirs=None,
                 s3_bucket=None, s3_prefix_data=None, s3_prefix_lookups=None,
                 parts_num=9999, data_file_format="json", lookup_file_format="json"):
        self.is_train = is_train
        self.history_col = history_col
        super().__init__(ctx_cols, seq_col, vl_col, label_col,
                 from_s3, local_data_dir, local_lookup_dirs,
                 s3_bucket, s3_prefix_data, s3_prefix_lookups,
                 parts_num, data_file_format, lookup_file_format)
        if self.history_col:
            self.history_np = np.concatenate(self.history_np, axis=0)

    def _valid_len(self, row):
        seq = row[self.seq_col]
        seq = [p for p in seq if p != 0]
        vl = len(seq)
        return vl

    def _append_np_from_df(self, df):
        # generate validate length col
        df[self.vl_col] = df.apply(self._valid_len, axis=1)
        # delete the rows where the validate length = 0
        df = df[df[self.vl_col] != 0]
        self.ctx_np.append(np.array(df[self.ctx_cols]))
        self.seq_np.append(np.array(df[self.seq_col].to_list()))
        self.vl_np.append(np.array(df[self.vl_col]))
        self.label_np.append(np.array(df[self.label_col].astype(float)))
        if self.history_col:
            self.history_np.append(np.array(df[self.history_col]))

    def _load_data_from_s3(self):
        # devide into train and test (little data)
        keys = []
        s3_client = boto3.client('s3')
        resp = s3_client.list_objects_v2(Bucket=self.s3_bucket, Prefix=self.s3_prefix_data)
        for obj in resp['Contents']:
            # for train or test
            if self.is_train:
                if obj['Key'].endswith(self.data_file_format) and "part-00148" not in obj['Key']:
                    keys.append(obj['Key'])
            else:
                if obj['Key'].endswith(self.data_file_format) and "part-00148" in obj['Key']:
                    keys.append(obj['Key'])
        for i, key in enumerate(keys):
            obj = s3_client.get_object(Bucket=self.s3_bucket, Key=key)
            df = self._read_df(obj['Body'], file_format=self.data_file_format)
            self._append_np_from_df(df)
            if i > self.parts_num:
                break

    def _load_data_from_local(self):
        # divide into train and test (little data)
        if self.is_train:
            f_paths = [
                os.path.join(self.local_data_dir, f_name)
                for f_name in os.listdir(self.local_data_dir)
                if f_name.endswith(self.data_file_format) and "part-00148" not in f_name
            ]
        else:
            f_paths = [
                os.path.join(self.local_data_dir, f_name)
                for f_name in os.listdir(self.local_data_dir)
                if f_name.endswith(self.data_file_format) and "part-00148" in f_name
            ]
        for i, f_path in enumerate(f_paths):
            df = self._read_df(f_path, self.data_file_format)
            self._append_np_from_df(df)
            if i > self.parts_num:
                break

    def get_feature_num(self, col):
        # TODO: implement via lookup dict
        # data_col = self.data[col]
        # if data_col.dtype == "int64":
        #     return data_col.astype(int).max() + 1
        if col == self.ctx_cols[0]:
            return int(self.ctx_np[:, 0].astype(int).max() + 1)
        elif col == self.ctx_cols[1]:
            return int(self.ctx_np[:, 1].astype(int).max() + 1)
        elif col == self.seq_col:
            return int(self.seq_np.reshape(-1).max()) + 1
        else:
            raise NotImplementedError()

    def export_lookups(self, local_dir, file_format):
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        for lookup_name, lookup_df in self.lookups.items():
            lookup_name = lookup_name.split("_")[0]
            output_path = os.path.join(local_dir, f"{lookup_name}.{file_format}")
            # add col names and change col dtype
            lookup_df.columns = ["value", "index"]
            lookup_df = lookup_df.astype({"value": str, "index": int})
            if file_format == "json":
                lookup_df.to_json(output_path)
            elif file_format == "csv":
                lookup_df.to_csv(output_path, index=False)
            else:
                raise NotImplementedError()


class PLTxT(LightningModule):
    def __init__(self, loss, optimizer, learning_rate, top_k, txt_kwargs):
        super().__init__()
        self.loss = loss
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.topk = top_k
        self.txt = TxT(**txt_kwargs)
        self.epoch_time = time.time()
        self.top_k_pos = self.top_k_neg = 0

    def forward(self, ctx_in, seq_in, vl_in):
        return self.txt(ctx_in, seq_in, vl_in)

    def forward_step(self, batch, phase):
        (ctx, seq, vl), label = batch
        out = self(
            ctx_in=ctx,
            seq_in=seq,
            vl_in=vl,
        )
        loss = self.loss(out, label.long())
        self.top_k_accuracy(out, label, self.topk)
        self.log(f"loss/{phase}", loss)
        return {"loss": loss,}

    def on_train_epoch_start(self):
        self.top_k_pos = self.top_k_neg = 0

    def training_step(self, batch, batch_idx):
        return self.forward_step(batch, "Train")

    def on_validation_epoch_start(self):
        if not self.trainer.sanity_checking:
            self.log("top_k/Train", self.top_k_pos / (self.top_k_pos + self.top_k_neg))
        self.top_k_pos = self.top_k_neg = 0

    def validation_step(self, batch, batch_idx):
        return self.forward_step(batch, "Validation")

    def on_validation_epoch_end(self):
        self.log("top_k/Validation", self.top_k_pos / (self.top_k_pos + self.top_k_neg))

    def configure_optimizers(self):
        return self.optimizer(self.parameters(), lr=self.learning_rate)

    def top_k_accuracy(self, output, target, topk):
        _, y_pred = torch.topk(output, topk, dim=1)
        target = target.view(-1, 1)
        self.top_k_pos += torch.eq(target, y_pred).sum()
        self.top_k_neg += target.size()[0] - torch.eq(target, y_pred).sum()
