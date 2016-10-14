"""GYPSY

Based on Hueng et all (2009)

Huang, S., Meng, S. X., & Yang, Y. (2009). A growth and yield projection system
(GYPSY) for natural and post-harvest stands in Alberta. Forestry Division,
Alberta Sustainable Resource Development, 25.

"""
import os
import matplotlib

# Force matplotlib to not use any Xwindows backend so that docker works
matplotlib.use('Agg')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

__all__ = ['DATA_DIR']
