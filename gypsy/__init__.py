"""GYPSY

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

import basal_area_increment

# Force matplotlib to not use any Xwindows backend so that docker works
matplotlib.use('Agg')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

__all__ = ['DATA_DIR', 'basal_area_increment']
