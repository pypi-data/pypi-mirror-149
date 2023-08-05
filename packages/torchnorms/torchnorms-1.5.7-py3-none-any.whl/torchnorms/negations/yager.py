# -*- coding: utf-8 -*-

import torch
from typing import Optional
from torch import nn, Tensor
from torch import isnan, tensor
from torch import sum as summer
from torchnorms.negations.base import BaseNegation


class YagerNegation(BaseNegation):
    def __init__(self,
                 p: Optional[Tensor] = None,
                 default_p: float = 1.1) -> None:
        super().__init__()
        self.p = p
        if self.p is None:
            assert default_p > -1
            self.p = nn.Parameter(torch.tensor(default_p))
        assert len(self.p.shape) == 0

        self.relu = torch.nn.ReLU()

        self.eps = 0.01
        self.__name__ = 'Yager'

    def __call__(self, a: Tensor) -> Tensor:
        self.adjust_nan_param()
        self.p.data = self.relu(self.p.data)
        if self.p == 0:
            self.p.data += self.eps

        res = torch.pow((1.0 - torch.pow(a, self.p)), 1.0 / self.p)

        return res

    def adjust_nan_param(self):
        for param in self.parameters():
            if summer(isnan(param)):
                low = -0.9 
                high = 10 
                new_init = (low - high)*torch.rand(1) + high  
                param.data = tensor(new_init, device = param.device)
