# copyright: (c) 2020 by Jesse Johnson.
# license: LGPL-3.0, see LICENSE.md for more details.
"""Provide system management for proman."""

import platform
from dataclasses import dataclass
from typing import Tuple


@dataclass
class System:
    """Provide system information."""

    arch: Tuple[str, str] = platform.architecture()
    kind: str = platform.system().lower()
