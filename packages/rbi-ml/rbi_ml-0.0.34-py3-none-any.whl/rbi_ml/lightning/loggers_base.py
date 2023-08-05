import numpy as np
import torch


def get_loss_scales(net, task1_criterion, task2_criterion, dataloader, device):
    net.eval()
    net.to(device)
    loss1_all = []
    loss2_all = []
    with torch.no_grad():
        for (ctx, seq, vl, candidate), (label_pos, label_price) in dataloader:
            out = net(
                ctx_in=[c.to(device) for c in ctx],
                seq_in=seq.to(device),
                vl_in=vl.to(device),
                candidate_in=candidate.to(device),
                seq_history=None
            )
            # print("*" * 10, f"torch.cuda.max_memory_allocated(): {torch.cuda.max_memory_allocated()}, "
            #       f"memory_allocated: {torch.cuda.memory_allocated()}", "*" * 10)
            loss1 = task1_criterion(out[0].squeeze(), label_pos.float().to(device))
            loss2 = task2_criterion(out[1].squeeze(), label_price.float().to(device))
            loss1_all.append(loss1.item())
            loss2_all.append(loss2.item())
    print("mean:", np.mean(loss1_all), np.mean(loss2_all))
    print("max:", np.max(loss1_all), np.max(loss2_all))
    loss1_scale = np.max(loss1_all)
    loss2_scale = np.max(loss2_all)
    return loss1_scale, loss2_scale


class BaseLogger:
    def __init__(self, metric):
        assert metric in ["acc", "f1", "mae", "mse", "loss", "identity"]
        self.metric_name = metric
        if metric == "acc":
            self.metric_fn = self.get_acc
        elif metric == "f1":
            self.metric_fn = self.get_f1
        elif metric == "mae":
            self.metric_fn = self.get_mae
        elif metric == "mse":
            self.metric_fn = self.get_mse
        elif metric == "identity" or metric == "loss":
            self.metric_fn = self.get_loss
        else:
            raise NotImplementedError()
        self.metrics_step = []

    def update(self, y_true, y_pred):
        self.metrics.append(self.metric_fn(y_true, y_pred))

    def get(self, reduce="mean"):
        if reduce == "mean":
            return np.mean(self.metrics)
        elif reduce == "count":
            return len(self.metrics)
        else:
            raise NotImplementedError()

    def reset(self):
        self.metrics = []

    @staticmethod
    def get_loss(loss, _):
        return loss.item()

    @staticmethod
    def get_acc(y_true: torch.Tensor, y_pred: torch.Tensor):
        return (y_true == y_pred).float().mean().item()

    @staticmethod
    def get_f1(y_true, y_pred, epsilon=1e-7):
        tp = (y_true * y_pred).sum().float()
        # tn = ((1 - y_true) * (1 - y_pred)).sum().float()
        fp = ((1 - y_true) * y_pred).sum().float()
        fn = (y_true * (1 - y_pred)).sum().float()
        precision = tp / (tp + fp + epsilon)
        recall = tp / (tp + fn + epsilon)
        f1 = 2 * (precision * recall) / (precision + recall + epsilon)
        return f1.item()

    @staticmethod
    def get_mae(y_true: torch.Tensor, y_pred: torch.Tensor):
        return (y_true - y_pred).abs().mean().item()

    @staticmethod
    def get_mse(y_true: torch.Tensor, y_pred: torch.Tensor):
        return (y_true - y_pred).pow(2).mean().item()


class MetricLogger:
    def __init__(self, names, metrics):
        self.metrics = {
            name: BaseLogger(metric=metric)
            for name, metric in zip(names, metrics)
        }

    def add(self, name, metric):
        self.metrics.update({name: metric})

    def update(self, metric_name, y_true, y_pred):
        if metric_name is None:
            for metric in self.metrics.values():
                metric.update(y_true, y_pred)
        else:
            self.metrics[metric_name].update(y_true, y_pred)

    def reset(self, metric_name):
        if metric_name is None:
            for metric in self.metrics.values():
                metric.reset()
        else:
            self.metrics[metric_name].reset()

    def get(self, metric_name, reduce="mean"):
        return self.metrics[metric_name].get(reduce=reduce)
