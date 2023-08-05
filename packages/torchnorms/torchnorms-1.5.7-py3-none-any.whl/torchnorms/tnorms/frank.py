# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor
from torch import isnan,tensor
from torch import sum as summer
from torchnorms.tnorms.base import BaseTNorm

from typing import Optional


class FrankTNorm(BaseTNorm):
    def __init__(self,
                 p: Optional[Tensor] = None,
                 default_p: float = 0.5) -> None:
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
        self.p.data = self.relu(self.p.data)

        if self.p == 0 or self.p == 1:
            self.p.data += self.eps

        res = 1.0 + ((torch.pow(self.p, a) - 1) * (torch.pow(self.p,b) - 1 ) / (self.p - 1.0))
        res = torch.log(res)

        # log base change trick -> change base to p
        res = res / torch.log(self.p)

        return res

    def adjust_nan_param(self):
        for param in self.parameters():
            if summer(isnan(param)):
                param.data = tensor(0.1, device = param.device)
