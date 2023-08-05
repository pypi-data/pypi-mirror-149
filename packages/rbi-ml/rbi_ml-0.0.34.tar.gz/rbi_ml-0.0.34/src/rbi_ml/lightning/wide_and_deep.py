import os
import time
import copy
import json
import boto3
import numpy as np
import pandas as pd
import wandb
import pytorch_lightning as pl
import torch
import torchmetrics
from pytorch_lightning import LightningModule
from torch.utils.data import Dataset, DataLoader
from ..models.wide_and_deep import WideAndDeep


class PLWideAndDeep(LightningModule):
    def __init__(self, loss, optimizer, learning_rate, lr_scheduler, lr_scheduler_kwargs, wad_kwargs):
        super().__init__()
        self.loss = loss
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.lr_scheduler = lr_scheduler
        self.lr_scheduler_kwargs = lr_scheduler_kwargs
        self.wad = WideAndDeep(**wad_kwargs)
        self.epoch_time = time.time()
        self.train_acc = torchmetrics.Accuracy()
        self.valid_acc = torchmetrics.Accuracy()

    def forward(self, wide_in, deep_in):
        return self.wad(wide_in, deep_in)

    def forward_step(self, batch, phase):
        (wide_in, deep_in), label = batch
        out = self(
            wide_in=wide_in,
            deep_in=deep_in,
        )
        out = torch.squeeze(out)
        label = label.float()
        loss = self.loss(out, label)
        if phase == "Train":
            self.train_acc(out, label.int())
            self.log(f"Accuracy/{phase}", self.train_acc, on_step=True, on_epoch=False)
        if phase == "Validation":
            self.valid_acc(out, label.int())
            self.log(f"Accuracy/{phase}", self.valid_acc, on_step=True, on_epoch=True)
        self.log(f"loss/{phase}", loss)
        return {"loss": loss,}

    def training_step(self, batch, batch_idx):
        return self.forward_step(batch, "Train")

    def validation_step(self, batch, batch_idx):
        return self.forward_step(batch, "Validation")

    def configure_optimizers(self):
        optimizer = self.optimizer(self.parameters(), lr=self.learning_rate)
        if self.lr_scheduler:
            lr_scheduler = self.lr_scheduler(optimizer, mode="min", verbose=True, **self.lr_scheduler_kwargs)
            return {
                "optimizer": optimizer,
                "lr_scheduler": {
                    "scheduler": lr_scheduler,
                    "monitor": "loss/Train",
                    "interval": "epoch"
                },
            }
        else:
            return optimizer


class WaDWandbArtifactCallback(pl.callbacks.Callback):
    def __init__(self, wandb_run, lookup_output_dir, torch_model_params, pl_model_params, model_dir):
        self.wandb_run = wandb_run
        self.model_dir = model_dir
        self.lookup_output_dir = lookup_output_dir
        self.torch_model_params = torch_model_params
        pl_model_params["loss"] = str(pl_model_params["loss"])
        pl_model_params["optimizer"] = str(pl_model_params["optimizer"])
        pl_model_params["lr_scheduler"] = str(pl_model_params["lr_scheduler"])
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
        torch.save(pl_module.wad.state_dict(), model_path)
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


class WaDTopKAccCallback(pl.callbacks.Callback):
    def __init__(self, test_dataset, top_k, device, logger):
        self.top_k = top_k
        self.device = device
        self.logger = logger
        test_dataset = copy.deepcopy(test_dataset)
        # remove negative sampled data points
        pos_idx = test_dataset.label_np == 1
        pos_candidates = test_dataset.candidate_np[pos_idx]
        all_candidates = np.unique(pos_candidates)
        num_all_candidates = len(all_candidates)
        # label will not be used when calculating metrics
        test_dataset.label_np = np.concatenate([np.zeros([len(pos_candidates), 1]) for _ in range(num_all_candidates)])
        curr_subtotal_np_pos = test_dataset.curr_subtotal_np[pos_idx]
        test_dataset.curr_subtotal_np = np.concatenate([curr_subtotal_np_pos for _ in range(num_all_candidates)])
        next_price_np_pos = test_dataset.next_price_np[pos_idx]
        test_dataset.next_price_np = np.concatenate([next_price_np_pos for _ in range(num_all_candidates)])
        ctx_np_pos = test_dataset.ctx_np[pos_idx]
        test_dataset.ctx_np = np.concatenate([ctx_np_pos for _ in range(num_all_candidates)])
        seq_np_pos = test_dataset.seq_np[pos_idx]
        test_dataset.seq_np = np.concatenate([seq_np_pos for _ in range(num_all_candidates)])
        vl_np_pos = test_dataset.vl_np[pos_idx]
        test_dataset.vl_np = np.concatenate([vl_np_pos for _ in range(num_all_candidates)])
        # loop thru every candidate
        test_dataset.candidate_np = np.concatenate([[all_candidates[i] for _ in range((len(pos_candidates)))]
                                                       for i in range(num_all_candidates)])

        if test_dataset.history_col:
            history_np_pos = test_dataset.history_np[pos_idx]
            test_dataset.history_np = np.concatenate([history_np_pos for _ in range(num_all_candidates)])
        test_dataset.len_data = len(test_dataset.ctx_np)
        self.pos_candidates = pos_candidates  # this will be used as target
        self.test_dataloader = DataLoader(test_dataset, batch_size=4096, num_workers=16, pin_memory=True)
        self.all_candidates = all_candidates
        self.num_all_candidates = num_all_candidates

    def on_validation_epoch_end(self, trainer, pl_module):
        # get predictions
        pl_module.eval()
        pl_module.to(self.device)
        preds = []
        with torch.no_grad():
            for (wide_in, deep_in), _ in self.test_dataloader:
                (ctx, (curr_subtotal, next_price)), (_, seq, vl, candidate) = wide_in, deep_in
                ctx_d = [c.to(self.device) for c in ctx]
                out = pl_module(
                    wide_in=(ctx_d, (curr_subtotal.to(self.device), next_price.to(self.device))),
                    deep_in=(ctx_d, seq.to(self.device), vl.to(self.device), candidate.to(self.device)),
                )
                preds.append(out.cpu().numpy())
        preds = np.concatenate(preds)
        # count top k
        top_k_purchased_total = top_k_unpurchased_total = 0
        for input_idx in range(len(self.pos_candidates)):
            pred_top_k_idx = np.argsort(preds[input_idx::len(self.pos_candidates)].flatten())[::-1]
            pred_top_k_candidate = [self.all_candidates[i] for i in pred_top_k_idx[:self.top_k]]
            if self.pos_candidates[input_idx] in pred_top_k_candidate:
                top_k_purchased_total += 1
            else:
                top_k_unpurchased_total += 1
        # calculate top k
        top_k_acc = top_k_purchased_total / (top_k_purchased_total + top_k_unpurchased_total)
        log_message = f"epoch: {pl_module.current_epoch}, " \
                      f"top_k_purchased_total: {top_k_purchased_total}, " \
                      f"top_k_unpurchased_total: {top_k_unpurchased_total}, " \
                      f"top_k_acc: {top_k_acc}"
        print(log_message)
        self.logger.info(log_message)
        wandb.log({'top_k_acc': top_k_acc})
        wandb.log({'top_k_purchased_total': top_k_purchased_total})
        wandb.log({'top_k_unpurchased_total': top_k_unpurchased_total})


class WaDOrderDataset(Dataset):
    """
    If from_s3 is True, will read data from s3. s3_bucket, s3_prefix_data and s3_prefix_lookups are required.
    Otherwise will read local data. local_data_data_dir and local_lookup_dirs are required.
    """
    def __init__(self, curr_subtotal_col, next_price_col, ctx_cols, seq_col, vl_col, candidate_col, history_col,
                 label_col, from_s3=True, local_data_dir=None, local_lookup_dirs=None,
                 s3_bucket=None, s3_prefix_data=None, s3_prefix_lookups=None,
                 parts_num=9999, data_file_format="json", lookup_file_format="json"):
        self.curr_subtotal_col = curr_subtotal_col
        self.next_price_col = next_price_col
        self.ctx_cols = ctx_cols
        self.seq_col = seq_col
        self.vl_col = vl_col
        self.candidate_col = candidate_col
        self.history_col = history_col
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
        self.curr_subtotal_np = []
        self.next_price_np = []
        self.ctx_np = []
        self.seq_np = []
        self.vl_np = []
        self.candidate_np = []
        self.label_np = []
        self.history_np = []
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
        self.curr_subtotal_np = np.concatenate(self.curr_subtotal_np, axis=0)
        self.next_price_np = np.concatenate(self.next_price_np, axis=0)
        self.ctx_np = np.concatenate(self.ctx_np, axis=0)
        self.seq_np = np.concatenate(self.seq_np, axis=0)
        self.vl_np = np.concatenate(self.vl_np, axis=0)
        self.candidate_np = np.concatenate(self.candidate_np, axis=0)
        self.label_np = np.concatenate(self.label_np, axis=0)
        if self.history_col:
            self.history_np = np.concatenate(self.history_np, axis=0)
        self.len_data = len(self.ctx_np)

    @staticmethod
    def _read_df(path, file_format):
        if file_format == "json":
            return pd.read_json(path, lines=True)
        elif file_format == "csv":
            return pd.read_csv(path)

    def _append_np_from_df(self, df):
        self.curr_subtotal_np.append(np.array(df[self.curr_subtotal_col].astype(np.float32)))
        self.next_price_np.append(np.array(df[self.next_price_col].astype(np.float32)))
        self.ctx_np.append(np.array(df[self.ctx_cols]))
        self.seq_np.append(np.array(df[self.seq_col].to_list()))
        self.vl_np.append(np.array(df[self.vl_col]))
        self.candidate_np.append(np.array(df[self.candidate_col]))
        self.label_np.append(np.array(df[self.label_col].astype(float)))
        if self.history_col:
            self.history_np.append(np.array(df[self.history_col]))

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
        curr_subtotal = self.curr_subtotal_np[idx]
        next_price = self.next_price_np[idx]
        ctx = [i for i in self.ctx_np[idx]]
        seq = torch.tensor(self.seq_np[idx])
        vl = self.vl_np[idx]
        candidate = self.candidate_np[idx]
        label = self.label_np[idx]
        if self.history_col:
            seq_history = torch.tensor(self.seq_np[idx])
            data = (ctx, (curr_subtotal, next_price)), (ctx, seq, vl, candidate, seq_history)
        else:
            data = (ctx, (curr_subtotal, next_price)), (ctx, seq, vl, candidate)
        return data, label

    def get_feature_num(self, col):
        if col == self.ctx_cols[0]:
            return int(self.ctx_np[:, 0].astype(int).max() + 1)
        elif col == self.ctx_cols[1]:
            return int(self.ctx_np[:, 1].astype(int).max() + 1)
        elif col == self.ctx_cols[2]:
            return int(self.ctx_np[:, 2].astype(int).max() + 1)
        elif col == self.seq_col:
            return int(max(int(self.seq_np.reshape(-1).max()), int(self.candidate_np.reshape(-1).max())) + 1)
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
