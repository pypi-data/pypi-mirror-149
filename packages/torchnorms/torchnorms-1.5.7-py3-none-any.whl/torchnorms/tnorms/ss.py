# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor
from torch import isnan,tensor
from torch import sum as summer
from torchnorms.tnorms.base import BaseTNorm

from typing import Optional


class SchweizerSklarTNorm(BaseTNorm):
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
        res: Optional[Tensor] = None
        # Careful that the value of parametr p can be 10e-8, thus maybe add eps.
        self.adjust_nan_param()
        self.p.data = self.relu(self.p.data)
        if self.p == 0:
            self.p.data += self.eps

        res = (a ** self.p + b ** self.p) - 1.0
        res = torch.maximum(res, torch.tensor(0.0))
        res = res ** (1.0 / self.p)

        if torch.sum(torch.isnan(res)):
            print(self.p)
            print(res)
            print("GANDON NAN")

        return res

    def adjust_nan_param(self):
        for param in self.parameters():
            if summer(isnan(param)):
                param.data = tensor(0.1, device = param.device)
