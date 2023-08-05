from collections import OrderedDict
from typing import Callable, Iterable, List, Optional, Union

import torch
import torch.nn as nn
import torchmetrics

from .utils.modules import ClassBundle


class Metrics(ClassBundle[torchmetrics.Metric]):

    def __init__(self, 
                 metrics: Iterable[torchmetrics.Metric] = None) -> None:
        if metrics is None:
            metrics = []
        super().__init__(metrics)
        self._metrics = self._objs

    def __call__(self, preds: torch.Tensor, targets: torch.Tensor) -> List[torch.Tensor]:
        results = []
        for m in self._metrics:
            results.append(m(preds, targets))
        return results

    @property
    def names(self) -> List[str]:
        return list(map(lambda m: m._get_name().lower(), self._metrics))

    def reset(self):
        for m in self._metrics:
            m.reset()

    def update(self, preds: torch.Tensor, targets: torch.Tensor) -> None:
        for m in self._metrics:
            m.update(preds, targets)

    def to_dict(self) -> OrderedDict:
        results = OrderedDict()
        for m in self._metrics:
            results[m._get_name().lower()] = m.compute().detach().cpu()
        return results

    def _apply(self, fn: Callable):
        for i, m in enumerate(self._metrics):
            self._metrics[i] = fn(m)
        return self
    
    def cuda(self, device: Optional[Union[int, torch.device]] = None):
        return self._apply(lambda t: t.cuda(device))

    def cpu(self):
        return self._apply(lambda t: t.cpu())

    def to(self, device: Union[str, torch.device]):
        return self._apply(lambda t: t.to(device=device))


class LossWrapper(torchmetrics.Metric):

    def __init__(self, loss: nn.Module):
        super().__init__()
        self.add_state("loss", default=[], dist_reduce_fx="cat")
        self._loss_func = loss

    def update(self, preds: torch.Tensor, targets: torch.Tensor):
        self.loss.append(self._loss_func(preds, targets))

    def compute(self) -> torch.Tensor:
        if len(self.loss) == 1:
            return self.loss[0].mean()
        else:
            return torch.cat(self.loss).mean()

    def _get_name(self):
        return "Loss"
