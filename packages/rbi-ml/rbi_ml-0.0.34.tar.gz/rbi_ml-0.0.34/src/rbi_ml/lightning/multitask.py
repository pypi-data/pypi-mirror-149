import copy
import os
import shutil
import time
import math
import json
import numpy as np
import pandas as pd
import boto3
import torch
import wandb
from torch.utils.data import Dataset, IterableDataset, DataLoader
import mlflow
import pytorch_lightning as pl
from pytorch_lightning.loggers import WandbLogger
from .callbacks_base import AttnVisCallbackBase, MLflowCallbackBase, TensorboardCallbackBase
from ..models.multitask import MultiTaskTxT, MultiTaskTxE
from pytorch_lightning import LightningModule


class MTWandbLogger(WandbLogger):
    def __init__(self, main_logger, task1_logger, task2_logger, loss_logger):
        super().__init__()
        self.main_logger = main_logger
        self.task1_logger = task1_logger
        self.task2_logger = task2_logger
        self.loss_logger = loss_logger


class MTMLflowCallback(MLflowCallbackBase):
    def __init__(self, model_dir, pl_params, model_name):
        self.model_dir = model_dir
        self.pl_params = pl_params
        self.model_name = model_name

    def update_mlflow_metrics(self, trainer, pl_module, phase):
        trainer_logger = trainer.logger
        trainer_loss_logger = trainer_logger.loss_logger
        trainer_task1_logger = trainer_logger.task1_logger
        trainer_task2_logger = trainer_logger.task2_logger
        mlflow.log_metrics(
            metrics={f"{phase}/loss": trainer_loss_logger.get("loss"),
                     f"{phase}/loss1": trainer_loss_logger.get("loss1"),
                     f"{phase}/loss2": trainer_loss_logger.get("loss2"),
                     f"{phase}/acc": trainer_task1_logger.get("acc"),
                     f"{phase}/f1": trainer_task1_logger.get("f1"),
                     f"{phase}/mae": trainer_task2_logger.get("mae"),
                     f"{phase}/mse": trainer_task2_logger.get("mse")},
            step=pl_module.current_epoch
        )

    def register_model(self, trainer, pl_module):
        mlflow.pytorch.log_model(
            pytorch_model=pl_module.multi_task,
            artifact_path="model",
            conda_env=None,
            registered_model_name=self.model_name,
            pip_requirements=[],
        )

    def log_artifacts_start(self, trainer, pl_module):
        mlflow.log_params(self.pl_params)

    def log_artifacts_epoch(self, trainer, pl_module):
        pass

    def log_artifacts_end(self, trainer, pl_module):
        mlflow.log_artifacts(local_dir=self.model_dir, artifact_path=None)


class MTTopKAccCallback(pl.callbacks.Callback):
    def __init__(self, test_dataset, top_k, device):
        self.top_k = top_k
        self.device = device
        test_dataset = copy.deepcopy((test_dataset))
        # remove negative sampled data points
        pos_idx = test_dataset.label_np[:, 0] == 1
        pos_candidates = test_dataset.candidate_np[pos_idx]
        all_candidates = np.unique(pos_candidates)
        num_all_candidates = len(all_candidates)
        # label will not be used when calculating metrics
        test_dataset.label_np = np.concatenate([np.zeros([len(pos_candidates), 2]) for _ in range(num_all_candidates)])
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
            for (ctx, seq, vl, candidate), (_, _) in self.test_dataloader:
                out = pl_module(
                    ctx_in=[c.to(self.device) for c in ctx],
                    seq_in=seq.to(self.device),
                    vl_in=vl.to(self.device),
                    candidate_in=candidate.to(self.device),
                    seq_history=None
                )
                preds.append(out[0].cpu().numpy())
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

        top_k_acc = top_k_purchased_total / (top_k_purchased_total + top_k_unpurchased_total)
        log_message = f"epoch: {pl_module.current_epoch+1}, " \
                      f"top_k_purchased_total: {top_k_purchased_total}, " \
                      f"top_k_unpurchased_total: {top_k_unpurchased_total}, " \
                      f"top_k_acc: {top_k_acc}"
        print(log_message)
        trainer.logger.main_logger.info(log_message)
        wandb.log({'top_k_acc': top_k_acc})
        wandb.log({'top_k_purchased_total': top_k_purchased_total})
        wandb.log({'top_k_unpurchased_total': top_k_unpurchased_total})


class MTWandbArtifactCallback(pl.callbacks.Callback):
    def __init__(self, wandb_run, lookup_output_dir, torch_model_params, pl_model_params, model_dir):
        self.wandb_run = wandb_run
        self.model_dir = model_dir
        self.lookup_output_dir = lookup_output_dir
        self.torch_model_params = torch_model_params
        pl_model_params["task1_criterion"] = str(pl_model_params["task1_criterion"])
        pl_model_params["task2_criterion"] = str(pl_model_params["task2_criterion"])
        pl_model_params["optimizer"] = str(pl_model_params["optimizer"])
        pl_model_params["multi_task_txt_kwargs"]["ctx_nums"] = [
            int(i) for i in pl_model_params["multi_task_txt_kwargs"]["ctx_nums"]
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
        torch.save(pl_module.multi_task.state_dict(), model_path)
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


class MTTensorboardCallback(TensorboardCallbackBase):
    def __init__(self, tensorboard_logger):
        super().__init__(tensorboard_logger)

    def update_metrics_scalar(self, trainer, pl_module, phase):
        epoch = pl_module.current_epoch
        trainer_logger = trainer.logger
        trainer_loss_logger = trainer_logger.loss_logger
        trainer_task1_logger = trainer_logger.task1_logger
        trainer_task2_logger = trainer_logger.task2_logger
        self.tensorboard_logger.experiment.add_scalar(f"loss1/{phase}", trainer_loss_logger.get("loss1"), epoch)
        self.tensorboard_logger.experiment.add_scalar(f"loss2/{phase}", trainer_loss_logger.get("loss2"), epoch)
        self.tensorboard_logger.experiment.add_scalar(f"loss/{phase}", trainer_loss_logger.get("loss"), epoch)
        self.tensorboard_logger.experiment.add_scalar(f"acc/{phase}", trainer_task1_logger.get("acc"), epoch)
        self.tensorboard_logger.experiment.add_scalar(f"f1/{phase}", trainer_task1_logger.get("f1"), epoch)
        self.tensorboard_logger.experiment.add_scalar(f"mae/{phase}", trainer_task2_logger.get("mae"), epoch)
        self.tensorboard_logger.experiment.add_scalar(f"mse/{phase}", trainer_task2_logger.get("mse"), epoch)


class MTContextAttnVisCallback(AttnVisCallbackBase):
    def __init__(self, transformer_prefix, cols, sample_inputs, device):
        super().__init__(transformer_prefix, cols, sample_inputs, device)

    def get_attn_weights(self, pl_module):
        ctx_embedding_layers = pl_module.multi_task.shared_bottom.context_transformer.ctx_embedding
        attn_layer = pl_module.multi_task.shared_bottom.context_transformer.ctx_encoder.layers[0].self_attn
        ctx_embedding_list = [ctx_embedding_layers[i](input_ctx.to(self.device)).unsqueeze(1)
                              for i, input_ctx in enumerate(self.sample_inputs)]
        ctx_out = torch.cat(ctx_embedding_list, dim=1)
        _, attn_weight = attn_layer(ctx_out, ctx_out, ctx_out, need_weights=True)
        avg_attn_weight = attn_weight.mean(0).mean(0).detach().tolist()
        return avg_attn_weight


class MTSequenceAttnVisCallback(AttnVisCallbackBase):
    def __init__(self, transformer_prefix, cols, sample_inputs, device):
        super().__init__(transformer_prefix, cols, sample_inputs, device)

    def get_attn_weights(self, pl_module):
        seq_in = self.sample_inputs[0].to(self.device)
        vl_in = self.sample_inputs[1].to(self.device)
        sequence_transformer_layer = pl_module.multi_task.shared_bottom.sequence_transformer
        attn_layer = pl_module.multi_task.shared_bottom.sequence_transformer.seq_encoder.layers[0].self_attn
        seq_out = sequence_transformer_layer.seq_embedding(seq_in.long())
        seq_out = seq_out * math.sqrt(sequence_transformer_layer.seq_embed_size)
        seq_out = sequence_transformer_layer.pos_encoder(seq_out)
        mask = sequence_transformer_layer.create_key_padding_mask(seq_in=seq_in, valid_length=vl_in)
        _, attn_weight = attn_layer(seq_out, seq_out, seq_out, key_padding_mask=mask, need_weights=True)
        avg_attn_weight = attn_weight.mean(0).mean(0).detach().tolist()
        return avg_attn_weight


class OrderDataset(Dataset):
    """
    If from_s3 is True, will read data from s3. s3_bucket, s3_prefix_data and s3_prefix_lookups are required.
    Otherwise will read local data. local_data_data_dir and local_lookup_dirs are required.
    """
    def __init__(self, ctx_cols, seq_col, vl_col, candidate_col, history_col, label_cols,
                 from_s3=True, local_data_dir=None, local_lookup_dirs=None,
                 s3_bucket=None, s3_prefix_data=None, s3_prefix_lookups=None,
                 parts_num=9999, data_file_format="json", lookup_file_format="json"):
        self.ctx_cols = ctx_cols
        self.seq_col = seq_col
        self.vl_col = vl_col
        self.candidate_col = candidate_col
        self.history_col = history_col
        self.label_cols = label_cols
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
        self.ctx_np.append(np.array(df[self.ctx_cols]))
        self.seq_np.append(np.array(df[self.seq_col].to_list()))
        self.vl_np.append(np.array(df[self.vl_col]))
        self.candidate_np.append(np.array(df[self.candidate_col]))
        self.label_np.append(np.array(df[self.label_cols].astype(float)))
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
        ctx = [i for i in self.ctx_np[idx]]
        seq = torch.tensor(self.seq_np[idx])
        vl = self.vl_np[idx]
        candidate = self.candidate_np[idx]
        labels = self.label_np[idx]
        if self.history_col:
            seq_history = torch.tensor(self.seq_np[idx])
            data = (ctx, seq, vl, candidate, seq_history)
        else:
            data = (ctx, seq, vl, candidate)
        return data, (labels[0], labels[1])

    def get_feature_num(self, col):
        # TODO: implement via lookup dict
        # data_col = self.data[col]
        # if data_col.dtype == "int64":
        #     return data_col.astype(int).max() + 1
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


class PLMultiTaskTxT(LightningModule):
    def __init__(self, task1_criterion, task2_criterion, optimizer, learning_rate,
                 loss_weights=(100, 1), log_interval=100,
                 multi_task_txt_model="MultiTaskTxT", multi_task_txt_kwargs=None):
        super().__init__()
        self.task1_criterion = task1_criterion
        self.task2_criterion = task2_criterion
        self.loss_weights = loss_weights
        self.log_interval = log_interval
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        if multi_task_txt_model == "MultiTaskTxT":
            self.multi_task = MultiTaskTxT(**multi_task_txt_kwargs)
        elif multi_task_txt_model == "MultiTaskTxE":
            self.multi_task = MultiTaskTxE(**multi_task_txt_kwargs)
        else:
            raise NotImplementedError()
        self.epoch_time = time.time()

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        return self.multi_task(ctx_in, seq_in, vl_in, candidate_in, seq_history)

    def forward_step(self, batch):
        (ctx, seq, vl, candidate), (label_pos, label_price) = batch
        out = self(
            ctx_in=ctx,
            seq_in=seq,
            vl_in=vl,
            candidate_in=candidate,
            seq_history=None
        )
        loss1 = self.task1_criterion(out[0].squeeze(), label_pos.float())
        loss2 = self.task2_criterion(out[1].squeeze(), label_price.float())
        loss = loss1 * self.loss_weights[0] + loss2 * self.loss_weights[1]
        y1_true = label_pos.float()
        y1_pred = (out[0].squeeze() > 0.5).float()
        y2_true = label_price.float()
        y2_pred = out[1].squeeze().float()
        return {"loss1": loss1.detach(), "loss2": loss2.detach(), "loss": loss,
                "y1_true": y1_true.detach(), "y1_pred": y1_pred.detach(),
                "y2_true": y2_true.detach(), "y2_pred": y2_pred.detach()}

    def on_train_epoch_start(self):
        self.reset_logger()

    def training_step(self, batch, batch_idx):
        return self.forward_step(batch)

    def training_step_end(self, step_output):
        self.update_logger(step_output)

    def on_validation_epoch_start(self):
        if not self.trainer.sanity_checking:
            self.write_logs("Train")
        self.reset_logger()

    def validation_step(self, batch, batch_idx):
        return self.forward_step(batch)

    def validation_step_end(self, step_output):
        self.update_logger(step_output)

    def on_validation_epoch_end(self):
        self.write_logs("Validation")

    def configure_optimizers(self):
        return self.optimizer(self.parameters(), lr=self.learning_rate)

    def update_logger(self, step_output):
        self.logger.task1_logger.update(metric_name=None, y_true=step_output["y1_true"], y_pred=step_output["y1_pred"])
        self.logger.task2_logger.update(metric_name=None, y_true=step_output["y2_true"], y_pred=step_output["y2_pred"])
        self.logger.loss_logger.update(metric_name="loss", y_true=step_output["loss"], y_pred=None)
        self.logger.loss_logger.update(metric_name="loss1", y_true=step_output["loss1"], y_pred=None)
        self.logger.loss_logger.update(metric_name="loss2", y_true=step_output["loss2"], y_pred=None)

    def reset_logger(self):
        self.epoch_time = time.time()
        self.logger.task1_logger.reset(metric_name=None)
        self.logger.task2_logger.reset(metric_name=None)
        self.logger.loss_logger.reset(metric_name=None)

    def write_logs(self, phase):
        log_str = "{} metrics Epoch {} Time elapsed {:.2f} - "\
                  "loss: {:.3f}, loss1: {:.3f}, loss2: {:.3f}, "\
                  "ACC: {:.2f}, F1: {:.2f}, MAE: {:.2f}, MSE: {:.2f}".format(
            phase, self.current_epoch + 1, time.time() - self.epoch_time,
            self.logger.loss_logger.get("loss"), self.logger.loss_logger.get("loss1"), self.logger.loss_logger.get("loss2"),
            self.logger.task1_logger.get("acc"), self.logger.task1_logger.get("f1"),
            self.logger.task2_logger.get("mae"), self.logger.task2_logger.get("mse"),
        )
        self.logger.main_logger.info(log_str)
