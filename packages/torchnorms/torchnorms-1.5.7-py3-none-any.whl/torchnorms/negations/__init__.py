# -*- coding: utf-8 -*-

from torchnorms.negations.base import *
from torchnorms.negations.classic import *
from torchnorms.negations.weber import *
from torchnorms.negations.yager import *

__all__ = [
    'BaseNegation',
    'StandardNegation',
    'AffineNegation',
    'StrictNegation',
    'StrictCosNegation',
    'WeberNegation',
    'YagerNegation'
]
