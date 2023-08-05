# -*- coding: utf-8 -*-

from torch import nn, Tensor
from torch import isnan,tensor
from torch import sum as summer

from abc import abstractmethod

import logging

logger = logging.getLogger(__name__)


class BaseTCoNorm(nn.Module):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def __call__(self,
              a: Tensor,
              b: Tensor) -> Tensor:
        raise NotImplementedError

    def norm(self,
               a: Tensor,
               b: Tensor) -> Tensor:
        return 1.0 - self(1.0 - a, 1.0 - b)

    def adjust_nan_param(self):
        for key, value in self.__dict__.items():
            if type(value) == nn.Parameter:
                if summer(isnan(value)):
                    print("The Value of the paramter became NAN")
                    value.data = tensor(0.1, device = value.device)
