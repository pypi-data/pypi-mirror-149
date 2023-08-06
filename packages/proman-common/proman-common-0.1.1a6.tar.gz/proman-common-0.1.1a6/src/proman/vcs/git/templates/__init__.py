# SPDX-FileCopyrightText: © 2020-2022 Jesse Johnson <jpj6652@gmail.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Provide templating capability."""

import os
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader


def render(data: Dict[str, Any], template_name: str) -> str:
    """Render template."""
    loader = FileSystemLoader(os.path.abspath(os.path.dirname(__file__)))
    env = Environment(loader=loader, autoescape=True)
    template = env.get_template(f"{template_name}.j2")
    content = template.render(**data)
    return content
