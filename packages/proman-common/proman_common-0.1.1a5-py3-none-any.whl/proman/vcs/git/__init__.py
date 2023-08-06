# copyright: Copyright (C) [2021] [Jesse P. Johnson]
# license: LGPL-3.0-or-later, see LICENSE.md for more details.
"""Provide common git capabilities."""

import logging
from typing import Any, List

from pygit2 import Repository

from .config import GitDirs
from .git import Git

__all__: List[str] = ['get_repo']

logging.getLogger(__name__).addHandler(logging.NullHandler())

project_dirs = GitDirs()


def get_repo(*args: Any, **kwargs: Any) -> Repository:
    """Create and return a release controller."""
    repo = Git(Repository(project_dirs.repo_dir))
    return repo
