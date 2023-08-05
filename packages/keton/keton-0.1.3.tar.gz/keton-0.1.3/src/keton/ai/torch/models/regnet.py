from collections import OrderedDict
from functools import partial

import torch
import torch.nn as nn
import torchvision

from torchvision.models.regnet import BlockParams, SimpleStemIN
from torchvision.models.regnet import model_urls

from .common import Model


__all__ = [
    "RegNet",
    "RegNetY400MF",
    "RegNetY800MF",
    "RegNetY1p6GF",
    "RegNetY3p2GF",
    "RegNetY8GF",
    "RegNetY16GF",
    "RegNetY32GF",
    "RegNetX400MF",
    "RegNetX800MF",
    "RegNetX1p6GF",
    "RegNetX3p2GF",
    "RegNetX8GF",
    "RegNetX16GF",
    "RegNetX32GF"
]


class RegNet(torchvision.models.RegNet, Model):

    ARCH: str = None

    def __init__(self, num_classes: int, in_channels: int = 3, pretrained: bool = False, **kwargs) -> None:
        self.num_classes = num_classes
        self.in_channels = in_channels

        stem_type = kwargs.get("stem_type", SimpleStemIN)
        stem_width = kwargs.get("stem_width", 32)
        norm_layer = kwargs.pop("norm_layer", partial(nn.BatchNorm2d, eps=1e-05, momentum=0.1))
        activation = kwargs.get("activation", nn.ReLU)
        torchvision.models.RegNet.__init__(self, num_classes=num_classes, norm_layer=norm_layer, **kwargs)
        if in_channels and in_channels != 3:
            self.stem = stem_type(in_channels, stem_width, norm_layer, activation)

        Model.__init__(self, pretrained=pretrained)

    def _load_pretrained_weights(self) -> None:
        if self.in_channels and self.in_channels != 3:
            raise ValueError(
                    f"Specifying input channels is not supported in pretrained model")
        state_dict = torch.hub.load_state_dict_from_url(model_urls[self.ARCH])
        for state_key in list(state_dict.keys()):
            module_name = state_key.split(".")[0]
            if module_name == "fc" and self.num_classes != 1000:
                state_dict.pop(state_key)
                continue
            if module_name not in self._pretrained_modules:
                self._pretrained_modules[module_name] = self.get_submodule(module_name)
        self.load_state_dict(state_dict, strict=False)

    @property
    def feature_modules(self) -> nn.ModuleDict:
        modules = nn.ModuleDict(OrderedDict(
            stem=self.stem,
            trunk_output=self.trunk_output
        ))
        return modules


class RegNetY400MF(RegNet):

    ARCH: str = "regnet_y_400mf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=16, w_0=48, w_a=27.89, w_m=2.09, group_width=8, se_ratio=0.25, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetY800MF(RegNet):

    ARCH: str = "regnet_y_800mf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=14, w_0=56, w_a=38.84, w_m=2.4, group_width=16, se_ratio=0.25, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetY1p6GF(RegNet):

    ARCH: str = "regnet_y_1_6gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=27, w_0=48, w_a=20.71, w_m=2.65, group_width=24, se_ratio=0.25, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetY3p2GF(RegNet):

    ARCH: str = "regnet_y_3_2gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=21, w_0=80, w_a=42.63, w_m=2.66, group_width=24, se_ratio=0.25, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetY8GF(RegNet):

    ARCH: str = "regnet_y_8gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=17, w_0=192, w_a=76.82, w_m=2.19, group_width=56, se_ratio=0.25, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetY16GF(RegNet):

    ARCH: str = "regnet_y_16gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=18, w_0=200, w_a=106.23, w_m=2.48, group_width=112, se_ratio=0.25, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetY32GF(RegNet):

    ARCH: str = "regnet_y_32gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=20, w_0=232, w_a=115.89, w_m=2.53, group_width=232, se_ratio=0.25, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetX400MF(RegNet):

    ARCH: str = "regnet_x_400mf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=22, w_0=24, w_a=24.48, w_m=2.54, group_width=16, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetX800MF(RegNet):

    ARCH: str = "regnet_x_800mf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=16, w_0=56, w_a=35.73, w_m=2.28, group_width=16, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetX1p6GF(RegNet):

    ARCH: str = "regnet_x_1_6gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=18, w_0=80, w_a=34.01, w_m=2.25, group_width=24, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetX3p2GF(RegNet):

    ARCH: str = "regnet_x_3_2gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=25, w_0=88, w_a=26.31, w_m=2.25, group_width=48, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetX8GF(RegNet):

    ARCH: str = "regnet_x_8gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=23, w_0=80, w_a=49.56, w_m=2.88, group_width=120, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetX16GF(RegNet):

    ARCH: str = "regnet_x_16gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=22, w_0=216, w_a=55.59, w_m=2.1, group_width=128, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)


class RegNetX32GF(RegNet):

    ARCH: str = "regnet_x_32gf"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        block_params = BlockParams.from_init_params(
            depth=23, w_0=320, w_a=69.86, w_m=2.0, group_width=168, **kwargs)
        super().__init__(num_classes,
                         in_channels=in_channels,
                         pretrained=pretrained,
                         block_params=block_params,
                         **kwargs)
