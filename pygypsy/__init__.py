"""pygypsy

Based on Hueng et all (2009)

Huang, S., Meng, S. X., & Yang, Y. (2009). A growth and yield projection system
(GYPSY) for natural and post-harvest stands in Alberta. Forestry Division,
Alberta Sustainable Resource Development, 25.

Important Acronyms:

aw = white aspen
sb = black spruce
sw = white spruce
pl = logdepole pine
bhage = Breast Height Age
tage = Total age
si_<xx> = estimated site index for species <xx>
y2bh = years until breast height age can be measured

"""
import os
import matplotlib
from ._version import get_versions

import pygypsy.basal_area_increment

__version__ = get_versions()['version']
del get_versions

# Force matplotlib to not use any Xwindows backend so that headless docker works
matplotlib.use('Agg')

__all__ = ['basal_area_increment']

