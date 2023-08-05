# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor
from torch import isnan,tensor
from torch import sum as summer
from torchnorms.tconorms.base import BaseTCoNorm

from typing import Optional


class SchweizerSklarTCoNorm(BaseTCoNorm):
    def __init__(self,
                 p: Optional[Tensor] = None,
                 default_p: float = 0.1) -> None:
        super().__init__()
        self.p = p
        if self.p is None:
            self.p = nn.Parameter(torch.tensor(default_p))

        assert len(self.p.shape) == 0

        self.eps = 0.001

    def __call__(self,
                 a: Tensor,
                 b: Tensor) -> Tensor:

        self.adjust_nan_param()

        if self.p == 0:
            self.p.data += self.eps

        p_1 = torch.pow(1.0 - a, self.p)
        p_2 = torch.pow(1.0 - b, self.p)
        p_1 = torch.maximum(torch.tensor(0), p_1 + p_2 - 1.0)
        res = torch.pow(p_1, 1.0 / self.p)
        res = 1.0 - res

        return res

    def adjust_nan_param(self):
        for param in self.parameters():
            if summer(isnan(param)):
                param.data = tensor(0.1, device = param.device)
