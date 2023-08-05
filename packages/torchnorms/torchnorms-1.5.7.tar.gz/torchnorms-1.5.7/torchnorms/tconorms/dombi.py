# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor
from torch import isnan, tensor
from torch import sum as summer

from torchnorms.tconorms.base import BaseTCoNorm

from typing import Optional


class DombiTCoNorm(BaseTCoNorm):
    def __init__(self,
                 p: Optional[Tensor] = None,
                 default_p: float = 0.1) -> None:
        super().__init__()
        self.p = p
        if self.p is None:
            self.p = nn.Parameter(torch.tensor(default_p))

        assert len(self.p.shape) == 0

        self.relu = torch.nn.ReLU()
        self.eps = 0.001

    def __call__(self,
                 a: Tensor,
                 b: Tensor) -> Tensor:

        self.adjust_nan_param()

        if self.p == 0:
            self.p.data += self.eps  # eps is added to avoid 0
        res = 1.0 - (((1 - a) * (1 - b)) / torch.maximum(torch.maximum(1.0 - a, 1.0 - b), self.p))
        return res

    def adjust_nan_param(self):
        for param in self.parameters():
            if summer(isnan(param)):
                param.data = tensor(0.1, device = param.device)
