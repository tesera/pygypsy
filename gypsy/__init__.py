"""teskelypy package
"""
import os
from .skel import has_legs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

__all__ = ['DATA_DIR']
