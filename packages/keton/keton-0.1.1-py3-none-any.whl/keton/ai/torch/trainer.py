from typing import Callable, Iterable, Optional, Union

import torch
import torch.nn as nn
import torch.optim as optim
import torchmetrics

from torch.utils.data import Dataset

from .metrics import Metrics, LossWrapper
from .callbacks import Callback, Callbacks, TqdmTrainLogger


class History(dict):

    def __init__(self) -> None:
        super().__init__()

    def _key(self, k: str, prefix: str) -> str:
        if prefix:
            k = f"{prefix}_{k}"
        return k

    def append(self, kv: dict, prefix: str = None) -> None:
        for k, v in kv.items():
            k = self._key(k, prefix)
            if k not in self:
                self[k] = []
            self[k].append(v)


class Trainer:

    def __init__(self,
                 model: nn.Module,
                 loss: nn.Module,
                 optimizer: optim.Optimizer,
                 metrics: Iterable[torchmetrics.Metric] = None,
                 device: Optional[Union[int, torch.device]] = None) -> None:

        self._model = model
        self._loss = loss
        self._optimizer = optimizer
        self._metrics = Metrics([LossWrapper(loss)])

        if metrics:
            self._metrics.append_all(metrics)

        self.device = device

        if device:
            self._apply(lambda t: t.to(device=device))

    def train(self,
              train_data: Dataset,
              batch_size: int = 32,
              epochs: int = 1,
              val_data: Dataset = None,
              callbacks: Iterable[Callback] = None,
              verbose: int = 1,
              description: str = None) -> History:
        # init history
        history = History()

        # init callbacks
        callbacks = self._init_callbacks(
            callbacks, verbose,
            epochs=epochs,
            steps_per_epoch=(len(train_data) + batch_size - 1) // batch_size,
            description=description
        )

        # train begin
        callbacks.on_train_begin()
        for e in range(1, epochs + 1):
            # epoch starts
            callbacks.on_epoch_begin(e)
            train_iter = torch.utils.data.DataLoader(train_data,
                                                     batch_size=batch_size, shuffle=True)
            # reset metrics and train on train batches
            callbacks.on_train_epoch_begin(e)
            self._metrics.reset()
            self._model.train()
            for b, (X, y) in enumerate(train_iter, 1):
                callbacks.on_train_batch_begin(b)
                if self.device:
                    X = X.to(device=self.device)
                    y = y.to(device=self.device)
                self._train_step(X, y)
                callbacks.on_train_batch_end(b, self._metrics.to_dict())
            callbacks.on_train_epoch_end(e, self._metrics.to_dict())
            history.append(self._metrics.to_dict())
            # reset metrics and validate on val batches
            if val_data is not None:
                callbacks.on_eval_begin(epoch=e)
                self._metrics.reset()
                self._model.eval()
                val_iter = torch.utils.data.DataLoader(
                    val_data, batch_size=batch_size)
                for b, (X, y) in enumerate(val_iter):
                    callbacks.on_eval_batch_begin(b)
                    if self.device:
                        X = X.to(device=self.device)
                        y = y.to(device=self.device)
                    self._eval_step(X, y)
                    callbacks.on_eval_batch_end(b, self._metrics.to_dict())
                callbacks.on_eval_end(self._metrics.to_dict(), epoch=e)
                history.append(self._metrics.to_dict(), prefix="val")
            # epoch ends
            callbacks.on_epoch_end(e)
        # train end
        callbacks.on_train_end()
        return history

    def _init_callbacks(self,
                        callbacks: Iterable[Callback],
                        verbose: int,
                        **params) -> Callbacks:
        callbacks = Callbacks(callbacks)
        if verbose == 1:
            callbacks.append(TqdmTrainLogger(log_on="step"))
        elif verbose == 2:
            callbacks.append(TqdmTrainLogger(log_on="epoch"))
        callbacks.set_model(self._model)
        callbacks.set_optimizer(self._optimizer)
        callbacks.set_params(params)
        return callbacks
    
    def _train_step(self, X: torch.Tensor, y: torch.Tensor):
        loss = self._metrics(self._model(X), y)[0]
        self._optimizer.zero_grad()
        loss.backward()
        self._optimizer.step()

    def _eval_step(self, X: torch.Tensor, y: torch.Tensor):
        with torch.no_grad():
            self._metrics.update(self._model(X), y)

    def _apply(self, fn: Callable):
        self._model = fn(self._model)
        self._loss = fn(self._loss)
        self._metrics = fn(self._metrics)
        return self

    def cuda(self, device: Optional[Union[int, torch.device]] = None):
        if isinstance(device, int):
            self.device = f"cuda:{device}"
        elif isinstance(device, torch.device):
            self.device = device
        else:
            self.device = "cuda"
        return self._apply(lambda t: t.cuda(device))

    def cpu(self):
        self.device = "cpu"
        return self._apply(lambda t: t.cpu())
