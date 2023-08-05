# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor
from torch import isnan,tensor
from torch import sum as summer
from torchnorms.tnorms.base import BaseTNorm

from typing import Optional


class AczelAlsinaTNorm(BaseTNorm):
    def __init__(self,
                 p: Optional[Tensor] = None,
                 default_p: float = 0.1) -> None:
        super().__init__()
        self.p = p
        if self.p is None:
            self.p = nn.Parameter(torch.tensor(default_p))

        else:
            assert self.p > 0
            assert self.p != float('inf')

        assert len(self.p.shape) == 0

        self.relu = torch.nn.ReLU()
        self.eps = 0.001

    def __call__(self,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        self.p.data = self.relu(self.p.data)
        if self.p == 0:
            self.p.data += self.eps

        #Taking the log here might be problamitc as some scores might be explicit 0's
        # Maybe we need to ofset by a small eps. i.e. 10^-4 ?
        p_1 = torch.pow(torch.abs(torch.log(a)), self.p)
        p_2 = torch.pow(torch.abs(torch.log(b)), self.p)
        res = torch.exp(-torch.pow(p_1 + p_2, 1.0 / self.p))
        
        return res

    def adjust_nan_param(self):
        for param in self.parameters():
            if summer(isnan(param)):
                param.data = tensor(0.1, device = param.device)
