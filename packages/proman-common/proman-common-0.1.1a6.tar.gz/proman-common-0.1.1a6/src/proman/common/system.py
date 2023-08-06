# SPDX-FileCopyrightText: © 2020-2022 Jesse Johnson <jpj6652@gmail.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Provide system management for proman."""

import platform
from dataclasses import dataclass
from typing import Tuple


@dataclass
class System:
    """Provide system information."""

    arch: Tuple[str, str] = platform.architecture()
    kind: str = platform.system().lower()
