from collections import OrderedDict

import torch
import torch.nn as nn
import torchvision

from torchvision.models.resnet import model_urls

from .common import Model


__all__ = [
    "ResNet",
    "ResNet10",
    "ResNet18",
    "ResNet34",
    "ResNet50",
    "ResNet101",
    "ResNet152"
]


class ResNet(torchvision.models.ResNet, Model):

    ARCH: str = None

    def __init__(self, num_classes: int, in_channels: int = 3, pretrained: bool = False, **kwargs) -> None:
        self.num_classes = num_classes
        self.in_channels = in_channels
        
        torchvision.models.ResNet.__init__(self, num_classes=num_classes, **kwargs)
        if in_channels and in_channels != 3:
            self.conv1 = torch.nn.Conv2d(
                in_channels, self.conv1.out_channels, kernel_size=7, stride=2, padding=3, bias=False)
        
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
            conv1=self.conv1,
            bn1=self.bn1,
            layer1=self.layer1,
            layer2=self.layer2,
            layer3=self.layer3,
            layer4=self.layer4
        ))
        return modules


class ResNet10(ResNet):

    ARCH: str = "resnet10"

    def __init__(self, num_classes: int, in_channels: int = None) -> None:
        super().__init__(num_classes,
                         in_channels=in_channels,
                         block=torchvision.models.resnet.BasicBlock,
                         layers=[1, 1, 1, 1])


class ResNet18(ResNet):

    ARCH: str = "resnet18"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained=False) -> None:
        super().__init__(num_classes,
                         in_channels=in_channels,
                         block=torchvision.models.resnet.BasicBlock,
                         layers=[2, 2, 2, 2],
                         pretrained=pretrained)


class ResNet34(ResNet):

    ARCH: str = "resnet34"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained=False) -> None:
        super().__init__(num_classes,
                         in_channels=in_channels,
                         block=torchvision.models.resnet.BasicBlock,
                         layers=[3, 4, 6, 3],
                         pretrained=pretrained)


class ResNet50(ResNet):

    ARCH: str = "resnet50"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained=False) -> None:
        super().__init__(num_classes,
                         in_channels=in_channels,
                         block=torchvision.models.resnet.Bottleneck,
                         layers=[3, 4, 6, 3],
                         pretrained=pretrained)


class ResNet101(ResNet):

    ARCH: str = "resnet101"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained=False) -> None:
        super().__init__(num_classes,
                         in_channels=in_channels,
                         block=torchvision.models.resnet.Bottleneck,
                         layers=[3, 4, 23, 3],
                         pretrained=pretrained)


class ResNet152(ResNet):

    ARCH: str = "resnet152"

    def __init__(self, num_classes: int, in_channels: int = None, pretrained=False) -> None:
        super().__init__(num_classes,
                         in_channels=in_channels,
                         block=torchvision.models.resnet.Bottleneck,
                         layers=[3, 8, 36, 3],
                         pretrained=pretrained)


