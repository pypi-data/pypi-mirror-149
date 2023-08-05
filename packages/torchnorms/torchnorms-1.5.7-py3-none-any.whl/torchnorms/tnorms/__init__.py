# -*- coding: utf-8 -*-

from torchnorms.tnorms.base import BaseTNorm
from torchnorms.tnorms.aa import AczelAlsinaTNorm
from torchnorms.tnorms.additive_generator import AdditiveLinearGenerator, AdditiveGenerator, AdditiveOrthogonalGenerator, AdditiveLearnableInverseGenerator, AdditivePolynomialGenerator
from torchnorms.tnorms.classic import MinimumTNorm, ProductTNorm, LukasiewiczTNorm, DrasticTNorm, EinsteinTNorm, BoundedTNorm, NilpotentMinimumTNorm, HamacherProductTNorm
from torchnorms.tnorms.dombi import DombiTNorm
from torchnorms.tnorms.dubois import DuboisTNorm
from torchnorms.tnorms.hamacher import HamacherTNorm
from torchnorms.tnorms.ss import SchweizerSklarTNorm
from torchnorms.tnorms.weber import WeberTNorm
from torchnorms.tnorms.yager import YagerTNorm
from torchnorms.tnorms.frank import FrankTNorm
from torchnorms.tnorms.laf import LearnableLatentTNorm
from torchnorms.tnorms.siamese_laf import LearnableSiameseLatentTNorm
__all__ = [
    'BaseTNorm',
    'AczelAlsinaTNorm',
    'AdditiveLinearGenerator',
    'AdditiveGenerator',
    'AdditiveOrthogonalGenerator',
    'AdditiveLearnableInverseGenerator',
    'AdditivePolynomialGenerator',
    'MinimumTNorm',
    'ProductTNorm',
    'LukasiewiczTNorm',
    'DrasticTNorm',
    'EinsteinTNorm',
    'BoundedTNorm',
    'NilpotentMinimumTNorm',
    'HamacherTNorm',
    'DombiTNorm',
    'DuboisTNorm',
    'HamacherProductTNorm',
    'SchweizerSklarTNorm',
    'WeberTNorm',
    'YagerTNorm',
    'FrankTNorm',
    'LearnableLatentTNorm',
    'LearnableSiameseLatentTNorm'
]
