# SPDX-FileCopyrightText: © 2020-2022 Jesse Johnson <jpj6652@gmail.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Provide exceptions."""

from typing import Any

from rich.traceback import install


class PromanException(Exception):
    """Provide base errors in project manager."""

    def __init__(self, message: str, **kwargs: Any) -> None:
        """Initialize exception."""
        formatting = kwargs.get('formatting', 'rich')
        if formatting == 'rich':
            show_locals = bool(kwargs.get('show_locals'))
            install(show_locals=show_locals)
        super().__init__(message)
