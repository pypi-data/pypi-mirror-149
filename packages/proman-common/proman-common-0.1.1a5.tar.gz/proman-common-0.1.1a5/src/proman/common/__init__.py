"""Common libraries for proman."""

import logging
from typing import List

logging.getLogger(__name__).addHandler(logging.NullHandler())

# package metadata
__author__ = 'Jesse P. Johnson'
__title__ = 'proman_common'
__version__ = '0.1.1a5'
__license__ = 'LGPL-3.0'
__all__: List[str] = ['GlobalDirs', 'AppDirs', 'SystemDirs', 'UserDirs']
