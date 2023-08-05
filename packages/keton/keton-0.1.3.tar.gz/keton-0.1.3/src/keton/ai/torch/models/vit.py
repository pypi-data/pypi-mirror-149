from collections import OrderedDict

import torch
import torch.nn as nn
import torchvision

from torchvision.ops.misc import ConvNormActivation
from torchvision.models.vision_transformer import model_urls

from .common import Model


__all__ = [
    "ViT",
    "ViTB16",
    "ViTB32",
    "ViTL16",
    "ViTL32"
]


class ViT(torchvision.models.VisionTransformer, Model):

    ARCH: str = None

    def __init__(self, num_classes: int, in_channels: int = 3, pretrained: bool = False, **kwargs) -> None:
        self.in_channels = in_channels

        torchvision.models.VisionTransformer.__init__(self,
                                                      image_size=kwargs.pop("image_size", 224),
                                                      num_classes=num_classes,
                                                      **kwargs)
        if in_channels and in_channels != 3:
            conv_stem_configs = kwargs.get("conv_stem_configs", None)
            if conv_stem_configs is not None:
                if len(conv_stem_configs) > 0:
                    self.conv_proj[0] = ConvNormActivation(
                        in_channels=in_channels,
                        out_channels=conv_stem_configs[0].out_channels,
                        kernel_size=conv_stem_configs[0].kernel_size,
                        stride=conv_stem_configs[0].stride,
                        norm_layer=conv_stem_configs[0].norm_layer,
                        activation_layer=conv_stem_configs[0].activation_layer,
                    )
                else:
                    self.conv_proj[0] = nn.Conv2d(
                        in_channels=in_channels, out_channels=self.hidden_dim, kernel_size=1)
            else:
                self.conv_proj = nn.Conv2d(
                    in_channels=in_channels, out_channels=self.hidden_dim,
                    kernel_size=self.patch_size, stride=self.patch_size)

        Model.__init__(self, pretrained=pretrained)

    def _load_pretrained_weights(self) -> None:
        if self.in_channels and self.in_channels != 3:
            raise ValueError(
                    f"Specifying input channels is not supported in pretrained model")
        state_dict = torch.hub.load_state_dict_from_url(model_urls[self.ARCH])
        for state_key in list(state_dict.keys()):
            module_name = state_key.split(".")[0]
            if module_name == "class_token":
                continue
            if module_name == "heads" and (self.representation_size or self.num_classes != 1000):
                state_dict.pop(state_key)
                continue
            if module_name not in self._pretrained_modules:
                self._pretrained_modules[module_name] = self.get_submodule(module_name)
        self.load_state_dict(state_dict, strict=False)
    
    @property
    def feature_modules(self) -> nn.ModuleDict:
        modules = nn.ModuleDict(OrderedDict(
            conv_proj=self.conv_proj,
            encoder=self.encoder
        ))
        return modules


class ViTB16(ViT):

    ARCH: str = "vit_b_16"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        super().__init__(num_classes,
                         patch_size=16,
                         num_layers=12,
                         num_heads=12,
                         hidden_dim=768,
                         mlp_dim=3072,
                         pretrained=pretrained,
                         **kwargs)


class ViTB32(ViT):

    ARCH: str = "vit_b_32"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        super().__init__(num_classes,
                         patch_size=32,
                         num_layers=12,
                         num_heads=12,
                         hidden_dim=768,
                         mlp_dim=3072,
                         pretrained=pretrained,
                         **kwargs)


class ViTL16(ViT):

    ARCH: str = "vit_l_16"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        super().__init__(num_classes,
                         patch_size=16,
                         num_layers=24,
                         num_heads=16,
                         hidden_dim=1024,
                         mlp_dim=4096,
                         pretrained=pretrained,
                         **kwargs)


class ViTL32(ViT):

    ARCH: str = "vit_l_32"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        super().__init__(num_classes,
                         patch_size=32,
                         num_layers=24,
                         num_heads=16,
                         hidden_dim=1024,
                         mlp_dim=4096,
                         pretrained=pretrained,
                         **kwargs)
