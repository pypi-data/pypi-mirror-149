"""Provide config management for git."""

import os
import sys
from dataclasses import dataclass, field
from typing import List

from pygit2 import discover_repository


@dataclass
class GitDirs:
    """Project package."""

    working_dir: str = os.getcwd()
    python_path: str = sys.executable
    repo_dir: str = field(init=False)
    info_dir: str = field(init=False)
    base_dir: str = field(init=False)
    project_dir: str = field(init=False)
    hooks_dir: str = field(init=False)
    templates_dir: str = field(init=False)
    container_build_dir: str = field(init=False)
    specfiles: List[str] = field(
        default_factory=lambda: ['pyproject.toml', 'setup.cfg'], repr=False
    )

    def __post_init__(self) -> None:
        """Initialize project settings."""
        if not hasattr(self, 'repo_dir') or self.repo_dir is None:
            self.repo_dir = discover_repository(os.getcwd())
        if not hasattr(self, 'base_dir'):
            self.base_dir = os.path.abspath(
                os.path.join(self.repo_dir, os.pardir)
            )
        if not hasattr(self, 'project_dir'):
            self.project_dir = os.path.abspath(
                os.path.join(self.repo_dir, os.pardir)
            )
        if not hasattr(self, 'info_dir'):
            self.info_dir = os.path.join(self.repo_dir, 'info')
        if not hasattr(self, 'hooks_dir'):
            self.hooks_dir = os.path.join(self.repo_dir, 'hooks')
        if not hasattr(self, 'templates_dir'):
            self.templates_dir = os.path.join(self.base_dir, 'templates')
        if not hasattr(self, 'container_build_dir'):
            self.container_build_dir = self.base_dir


@dataclass
class GitIgnoreConfig(GitDirs):
    """Configure gitignore."""

    source: str = os.path.join(
        os.path.dirname(__file__), '_vendor', 'gitignore'
    )
    destination: str = field(init=False)
    include_files: List = field(
        default_factory=lambda: ['Python.gitignore', 'Global/Vim.gitignore']
    )

    def __post_init__(self) -> None:
        """Initialize gitignore settings."""
        super().__post_init__()
        if not hasattr(self, 'destination'):
            self.destination = os.path.join(self.info_dir, 'exclude')
