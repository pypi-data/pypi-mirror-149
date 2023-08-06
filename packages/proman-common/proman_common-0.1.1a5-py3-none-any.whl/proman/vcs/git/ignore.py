# copyright: (c) 2021 by Jesse Johnson.
# license: LGPL-3.0-or-later, see LICENSE.md for more details.
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
