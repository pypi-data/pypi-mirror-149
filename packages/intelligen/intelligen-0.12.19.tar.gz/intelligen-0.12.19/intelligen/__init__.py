"""Top-level package for intelligen."""

__author__ = """Diego Bouchet"""
__email__ = 'diegobouchet88@gmail.com'
__version__ = '0.12.19'

submodules = [
        'AI',
        'constants',
        'integrate',
        'intelligen',
        'interpolate',
        'linregress',
        'numeric',
        'signals',
        'stats'
    ]

__all__ = submodules

from . import AI
from . import constants
from . import integrate
from . import intelligen
from . import interpolate
from . import linregress
from . import numeric
from . import signals
from . import stats
