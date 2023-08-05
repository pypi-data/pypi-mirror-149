# -*- coding: utf-8 -*-

from torch import nn, Tensor
from torch import isnan,tensor
from abc import abstractmethod
from torch import sum as summer

import logging

logger = logging.getLogger(__name__)


class BaseNegation(nn.Module):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def __call__(self,
                 a: Tensor) -> Tensor:
        raise NotImplementedError

    def adjust_nan_param(self):
        for key, value in self.__dict__.items():
            if type(value) == nn.Parameter:
                if summer(isnan(value)):
                    print("The Value of the paramter became NAN")
                    value.data = tensor(0.1, device=value.device)
