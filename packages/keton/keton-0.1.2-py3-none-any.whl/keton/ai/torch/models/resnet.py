import torch
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

    def __init__(self, num_classes: int, in_channels: int = None, pretrained: bool = False, **kwargs) -> None:
        torchvision.models.ResNet.__init__(self, **kwargs)
        Model.__init__(self, pretrained=pretrained)

        if num_classes != self.fc.out_features:
            if pretrained:
                self._pretrained_modules.pop("fc")
            self.fc = torch.nn.Linear(self.fc.in_features, num_classes)
        if in_channels and in_channels != self.conv1.in_channels:
            if pretrained:
                raise ValueError(
                    f"Specifying input channels is not supported in pretrained model")
            self.conv1 = torch.nn.Conv2d(
                in_channels, self.conv1.out_channels, kernel_size=7, stride=2, padding=3, bias=False)

    def _load_pretrained_weights(self) -> None:
        state_dict = torch.hub.load_state_dict_from_url(model_urls[self.ARCH])
        self.load_state_dict(state_dict)
        for state_key in state_dict:
            module_name = state_key.split(".")[0]
            if module_name not in self._pretrained_modules:
                self._pretrained_modules[module_name] = self.get_submodule(module_name)


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


