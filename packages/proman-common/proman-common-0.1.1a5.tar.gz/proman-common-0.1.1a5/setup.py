# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['proman',
 'proman.common',
 'proman.vcs',
 'proman.vcs.git',
 'proman.vcs.git.templates']

package_data = \
{'': ['*'],
 'proman.vcs.git': ['_vendor/*',
                    '_vendor/gitignore/*',
                    '_vendor/gitignore/.github/*',
                    '_vendor/gitignore/Global/*',
                    '_vendor/gitignore/community/*',
                    '_vendor/gitignore/community/AWS/*',
                    '_vendor/gitignore/community/DotNet/*',
                    '_vendor/gitignore/community/Elixir/*',
                    '_vendor/gitignore/community/GNOME/*',
                    '_vendor/gitignore/community/Golang/*',
                    '_vendor/gitignore/community/Java/*',
                    '_vendor/gitignore/community/JavaScript/*',
                    '_vendor/gitignore/community/Linux/*',
                    '_vendor/gitignore/community/PHP/*',
                    '_vendor/gitignore/community/Python/*',
                    '_vendor/gitignore/community/embedded/*',
                    'grammars/*']}

install_requires = \
['compendium[toml]>=0.1.1-alpha.0,<0.2.0',
 'keyring>=23.0.1,<24.0.0',
 'rich>=12.0.1,<13.0.0']

extras_require = \
{'gnome:sys_platform == "linux"': ['SecretStorage>=3.3.1,<4.0.0'],
 'kde:sys_platform == "linux"': ['dbus-python>=1.2.16,<2.0.0']}

setup_kwargs = {
    'name': 'proman-common',
    'version': '0.1.1a5',
    'description': 'GitHub based package manager.',
    'long_description': '# pkgmgr-github\n\n[![License](https://img.shields.io/badge/License-LGPL%203.0-blue.svg)](https://spdx.org/licenses/LGPL-3.0)\n[![Build Status](https://travis-ci.org/kuwv/pkgmgr-github.svg?branch=master)](https://travis-ci.org/kuwv/pkgmgr-github)\n[![codecov](https://codecov.io/gh/kuwv/pkgmgr-github/branch/master/graph/badge.svg)](https://codecov.io/gh/kuwv/pkgmgr-github)\n\n## Overview\n\nGitHub based package manager.\n\n## Install\n\n`pip install proman.common`\n',
    'author': 'Jesse P. Johnson',
    'author_email': 'jpj6652@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-proman/proman-common',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
