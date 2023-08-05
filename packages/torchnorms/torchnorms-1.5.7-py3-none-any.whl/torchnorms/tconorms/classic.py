# -*- coding: utf-8 -*-

import torch
from torch import Tensor

from torchnorms.tconorms.base import BaseTCoNorm


class MinimumCoNorm(BaseTCoNorm):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __call__(cls,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        return torch.maximum(a, b)


class ProductTCoNorm(BaseTCoNorm):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __call__(cls,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        return 1 - ((1 - a) * (1 - b))


class LukasiewiczTCoNorm(BaseTCoNorm):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __call__(cls,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        # Careful not to overbroadcast
        return torch.minimum(a + b, torch.tensor(1.0))


class EinsteinTCoNorm(BaseTCoNorm):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __call__(cls,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        return (a + b) / (1.0 + (a * b))


class BoundedTCoNorm(BaseTCoNorm):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __call__(cls,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        return torch.minimum(torch.tensor(1), a + b)


class NilpotentMinimumTCoNorm(BaseTCoNorm):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def __call__(cls,
                 a: Tensor,
                 b: Tensor) -> Tensor:

        mask = (a+b) < 1.0
        res = torch.max(a,b) * mask
        zero_ind = (res == 0).nonzero()
        res[zero_ind] = 1.0

        return res
