"""teskelypy package
"""
import os
from .skel import has_legs
import matplotlib

# Force matplotlib to not use any Xwindows backend so that docker works
matplotlib.use('Agg')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

__all__ = ['DATA_DIR']
