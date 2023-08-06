"""
Collection of physical constants and conversion factors
"""

import numpy as np

__all__ = ['golden', 'golden_ratio', 'igolden', 'inverse_golden_ratio',
           'G', 'g', 'c', 'speed_of_light', 'yotta', 'zetta', 'exa',
           'peta', 'tera', 'giga', 'mega', 'mega', 'kilo', 'hecto',
           'deka', 'deci', 'centi', 'milli', 'micro', 'nano', 'pico',
           'femto', 'atto', 'zepto', 'yocto']

golden = golden_ratio = (1 + np.sqrt(5))/2
igolden = inverse_golden_ratio = (1 - np.sqrt(5))/2

G = 6.67430e-11
g = 9.807
c = speed_of_light = 299_792_458

# SI prefixes
yotta = 1e24
zetta = 1e21
exa = 1e18
peta = 1e15
tera = 1e12
giga = 1e9
mega = 1e6
kilo = 1e3
hecto = 1e2
deka = 1e1
deci = 1e-1
centi = 1e-2
milli = 1e-3
micro = 1e-6
nano = 1e-9
pico = 1e-12
femto = 1e-15
atto = 1e-18
zepto = 1e-21
yocto = 1e-24