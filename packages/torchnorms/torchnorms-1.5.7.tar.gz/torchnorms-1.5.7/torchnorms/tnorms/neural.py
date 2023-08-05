# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor

from torchnorms.tnorms.base import BaseTNorm


class NeuralSiameseTNorm(BaseTNorm):
    def __init__(self) -> None:
        super().__init__()
        self.model = nn.Linear(in_features=1, out_features=1, bias=True)

    def __call__(self,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        return self.model(a) * self.model(b)


class NeuralTNorm(BaseTNorm):
    def __init__(self) -> None:
        super().__init__()
        self.model = nn.Linear(in_features=2, out_features=1, bias=True)

    def __call__(self,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        return self.model(a) * self.model(b)
