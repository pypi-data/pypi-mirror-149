import torch
from .utils import rename
import torch.nn.functional as F
import numpy as np
from copy import deepcopy

class MetricBase:
    """
    把每个batch的预测和标签记录下来，可能点用很大存储空间。
    """
    def __init__(self, metric_fn=None, name=None):
        self.name = self.__class__.__name__ if name is None else name
        if metric_fn:
            self.metric_fn = metric_fn
        else:
            self.metric_fn = self.forward
        self.pred_batchs = []
        self.target_batchs = []

    def __call__(self, preds, targets):
        self.update(preds, targets)
        return self.metric_fn(preds, targets)

    def forward(self, preds, targets):
        return NotImplemented
    
    def update(self, preds, targets):
        self.pred_batchs.append(preds)
        self.target_batchs.append(targets)

    def reset(self):
        self.pred_batchs = []
        self.target_batchs = []

    def compute(self):
        pred_epoch = torch.concat(self.pred_batchs)
        target_epoch = torch.concat(self.target_batchs)
        return self.metric_fn(pred_epoch, target_epoch)

    def clone(self):
        return deepcopy(self)


@rename('acc')
def accuracy(out, yb):
    return (torch.argmax(out, dim=1) == yb).float().mean()


@rename('acc')
def masked_accuracy(preds, targets):
    _, preds = preds.max(dim=1)
    correct = preds[targets.mask].eq(targets.data[targets.mask]).sum()
    acc = correct / targets.mask.float().sum()
    return acc


@rename('mse')
def masked_mse(preds, targets):
    return F.mse_loss(torch.squeeze(preds[targets.mask]), targets.data[targets.mask])


@rename('mae')
def masked_mae(preds, targets):
    preds = torch.squeeze(preds[targets.mask])
    targets = targets.data[targets.mask]
    return torch.mean(torch.abs(preds - targets))


def ordinal(preds, targets):
    """
    真实排序下，对应的预测值的序号
    """
    frame = np.array([preds, targets]).transpose()
    frame = frame[(-frame[:, 0]).argsort()]
    frame = np.concatenate([frame, np.expand_dims(np.arange(1, len(preds)+1), 1)], 1)
    frame = frame[(-frame[:, 1]).argsort()]
    preds_ids = frame[:, 2]
    return preds_ids


@rename('map')
def MAP(preds, targets):
    """
    Mean average precision(MAP)
    """
    n = len(preds)
    targets_ids = np.arange(1, len(preds)+1)
    preds_ids = ordinal(preds, targets)

    def p_at_n(p_ids, t_ids, n):
        return len(set(p_ids[:n]).intersection(set(t_ids[:n])))/n
    return np.average([p_at_n(preds_ids, targets_ids, i) for i in range(1, n+1)])


@rename('map')
def masked_MAP(preds, targets):
    """
    Mean average precision(MAP)
    """
    preds = torch.squeeze(preds[targets.mask]).detach().cpu().numpy()
    targets = targets.data[targets.mask].detach().cpu().numpy()
    return MAP(preds, targets)


def DCG_at_n(preds, targets, n):
    """
    Discount Cumulative Gain (DCG@n)
    """
    frame = np.array([preds, targets]).transpose()
    frame = frame[(-frame[:, 0]).argsort()]
    frame = frame[:n]
    return np.sum([t/np.log2(i+2) for i, (_, t) in enumerate(frame)])


def NDCG_at_n(n, preds, targets):
    """
    Normalized discount cumulative gain (NDCG@n)
    """
    return DCG_at_n(preds, targets, n)/DCG_at_n(targets, targets, n)


def masked_NDCG_at_n(n, preds, targets):
    """
    Masked normalized discount cumulative gain (NDCG@n)
    """
    preds = torch.squeeze(preds[targets.mask]).detach().cpu().numpy()
    targets = targets.data[targets.mask].detach().cpu().numpy()
    return NDCG_at_n(n, preds, targets)
