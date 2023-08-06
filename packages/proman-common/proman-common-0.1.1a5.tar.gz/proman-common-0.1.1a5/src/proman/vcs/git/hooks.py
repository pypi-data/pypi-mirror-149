"""Provide templating for git hooks."""

import os
import shutil
from typing import List

from . import templates


class Hooks:
    """Manage git hooks."""

    def __init__(self, hooks_dir: str) -> None:
        """Initialize hooks object."""
        self.hooks_dir = hooks_dir

    @property
    def hooks(self) -> List[str]:
        """List git hooks."""
        hooks = [
            x for x in os.listdir(self.hooks_dir) if not x.endswith('sample')
        ]
        return hooks

    def setup(self, name: str = 'pre-commit', update: bool = False) -> None:
        """Create git hook."""
        path = os.path.join(self.hooks_dir, name)
        if update or not os.path.exists(path):
            data = {
                'executable': shutil.which('project'),
                'hook': name,
            }
            templates.render(
                data,
                template_name='githooks',
                # dest=path,
                # executable=True,
                # update=update,
            )

    def remove(self, name: str = 'pre-commit') -> None:
        """Remove git hook."""
        path = os.path.join(self.hooks_dir, name)
        if os.path.exists(path):
            os.remove(path)
