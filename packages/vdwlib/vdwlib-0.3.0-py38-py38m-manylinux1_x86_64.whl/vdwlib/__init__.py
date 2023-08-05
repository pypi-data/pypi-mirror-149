'''
# vdwlib
Van der Waals radii library

'''

from .__version__ import __title__, __url__, __version__, __description__
from .__version__ import __build__, __author__, __license__, __copyright__

from .radii import *

__all__ = []
__all__ += radii.__all__
