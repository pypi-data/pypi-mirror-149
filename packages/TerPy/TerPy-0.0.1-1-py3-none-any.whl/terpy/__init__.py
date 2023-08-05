'''
    Terpy
    ~~~~~

    Computational chemistry utilities
'''

from .__version__ import __version__
from .__version__ import __author__

from . import structures
from .structures import *

__all__ = []
__all__ += structures.__all__
