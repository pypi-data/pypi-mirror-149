# SPDX-FileCopyrightText: © 2020-2022 Jesse Johnson <jpj6652@gmail.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Common libraries for proman."""

import logging
from typing import List

logging.getLogger(__name__).addHandler(logging.NullHandler())

# package metadata
__author__ = 'Jesse P. Johnson'
__title__ = 'proman_common'
__version__ = '0.1.1a6'
__license__ = 'LGPL-3.0'
__all__: List[str] = ['GlobalDirs', 'AppDirs', 'SystemDirs', 'UserDirs']
