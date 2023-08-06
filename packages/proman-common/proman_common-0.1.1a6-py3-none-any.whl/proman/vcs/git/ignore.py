# SPDX-FileCopyrightText: © 2020-2022 Jesse Johnson <jpj6652@gmail.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Provide project initialization."""

import logging
import os
# import shutil
from typing import TYPE_CHECKING, Any, Dict  # noqa

from .config import GitIgnoreConfig

logging.getLogger(__name__).addHandler(logging.NullHandler())


class GitIgnore:
    """Check gitignore setup."""

    def __init__(self, config: 'GitIgnoreConfig' = GitIgnoreConfig()) -> None:
        """Initialize gitignore."""
        self.__settings = config

    def setup(self) -> None:
        """Create gitignore file."""
        with open(self.__settings.destination, 'w') as ignore_file:
            for x in self.__settings.include_files:
                source_file = os.path.join(self.__settings.source, x)
                with open(source_file) as f:
                    for line in f:
                        ignore_file.write(line)
