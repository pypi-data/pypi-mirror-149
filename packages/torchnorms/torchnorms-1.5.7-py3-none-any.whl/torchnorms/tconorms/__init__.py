# -*- coding: utf-8 -*-

from torchnorms.tconorms.base import *
from torchnorms.tconorms.classic import *
from torchnorms.tconorms.dombi import *
from torchnorms.tconorms.dubois import *
from torchnorms.tconorms.hamacher import *
from torchnorms.tconorms.ss import *
from torchnorms.tconorms.weber import *
from torchnorms.tconorms.yager import *

__all__ =[
    'BaseTCoNorm',
    'BoundedTCoNorm',
    'DombiTCoNorm',
    'DuboisTCoNorm',
    'EinsteinTCoNorm',
    'HamacherTCoNorm',
    'LukasiewiczTCoNorm',
    'MinimumCoNorm',
    'NilpotentMinimumTCoNorm',
    'ProductTCoNorm',
    'SchweizerSklarTCoNorm',
    'WeberTCoNorm',
    'YagerTCoNorm',
]
