# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor
from torch import isnan,tensor
from torch import sum as summer
from torchnorms.tnorms.base import BaseTNorm

from typing import Optional


class DombiTNorm(BaseTNorm):
    def __init__(self,
                 p: Optional[Tensor] = None,
                 default_p: float = 0.1) -> None:
        super().__init__()
        self.p = p
        if self.p is None:
            self.p = nn.Parameter(torch.tensor(default_p))
        assert len(self.p.shape) == 0
        self.relu = torch.nn.ReLU()
        self.eps = 0.01

    def __call__(self,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        self.adjust_nan_param()
        self.p.data = self.relu(self.p.data)

        if self.p == 0:
            # eps is added to avoid 0
            self.p.data += self.eps

        p_1 = torch.pow((1 - a) / a, self.p)
        p_2 = torch.pow((1 - b) / b, self.p)
        p_3 = 1.0 + torch.pow(p_1 + p_2, 1.0 / self.p)
        res = 1.0 / p_3

        return res

    def adjust_nan_param(self):
        for param in self.parameters():
            if summer(isnan(param)):
                param.data = tensor(0.1, device = param.device)
