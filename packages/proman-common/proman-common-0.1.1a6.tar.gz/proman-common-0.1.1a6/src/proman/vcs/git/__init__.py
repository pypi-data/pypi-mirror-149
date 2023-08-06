# SPDX-FileCopyrightText: © 2020-2022 Jesse Johnson <jpj6652@gmail.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Provide common git capabilities."""

import logging
from typing import Any, List

from pygit2 import Repository

from .config import GitDirs
from .git import Git

__all__: List[str] = ['get_repo']

logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_repo(*args: Any, **kwargs: Any) -> Repository:
    """Create and return a release controller."""
    project_dirs = GitDirs()
    repo = Git(Repository(project_dirs.repo_dir))
    return repo
