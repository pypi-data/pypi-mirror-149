import collections
from typing import OrderedDict


import torch.nn as nn


class Model:

    _pretrained_modules: OrderedDict[str, nn.Module]

    def __init__(self, pretrained: bool = False) -> None:
        self._pretrained_modules = collections.OrderedDict()
        if pretrained:
            self._load_pretrained_weights()

    def _load_pretrained_weights(self) -> None:
        raise NotImplementedError(
            f"Model '{self.__class__.__name__}' is not supported")

    @property
    def pretrained_modules(self) -> nn.ModuleDict:
        return nn.ModuleDict(self._pretrained_modules)

    @property
    def feature_modules(self) -> nn.ModuleDict:
        raise NotImplementedError(
            f"Model '{self.__class__.__name__}' is not supported")
