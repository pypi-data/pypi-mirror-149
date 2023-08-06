# copyright: (c) 2020 by Jesse Johnson.
# license: LGPL-3.0-or-later, see LICENSE.md for more details.
"""Control Git submodules."""

import os
from typing import TYPE_CHECKING, List, Optional

from pygit2 import Keypair, RemoteCallbacks, Repository

from . import filesystem
from . import config

if TYPE_CHECKING:
    from pygit2 import Submodule

# TODO: refactor
# post_commit = """#!/bin/bash
# exec git submodule update
# """


# def setup() -> None:
#     """Do setup for post checkout hooks."""
#     path = os.path.join(os.getcwd(), '.git', 'hooks', 'post-checkout')
#     with open(path, 'w') as f:
#         f.write(post_commit)


class Submodule:
    def index():  # type: () -> List[Submodule]
        """List submodules with project."""
        submodules = repo().listall_submodules()
        print(submodules)
        return submodules

    def info(name):  # type: (str) -> None
        """View project info."""
        sm = repo().submodule(name)
        print(sm.children())

    def remove(name):  # type: (str) -> None
        """Remove submodule from repository."""
        data = config.load()
        if 'submodule' in data:
            # remove configuration
            submodule = data['submodule'].pop(name)
            if data != {}:
                config.dump(
                    data,
                    template_name='gitconfig',
                    dest=os.path.join(.repo_dir, 'config'),
                    update=update,
                )
        else:
            raise Exception('no submodules found within project')

        gitmodules_path = os.path.join(.project_dir, '.gitmodules')
        if os.path.exists(gitmodules_path):
            data = config.load(gitmodules_path)
            if 'submodule' in data:
                # remove configuration
                submodule = data['submodule'].pop(name)
                if data != {}:
                    config.dump(
                        ,
                        data,
                        template_name='gitconfig',
                        dest=gitmodules_path,
                        update=update,
                    )
                else:
                    filesystem.rm(gitmodules_path)

                # remove submodule directory from git repo
                filesystem.rm(
                    os.path.join(.repo_dir, 'modules', submodule['path'])
                )

                # remove submodule from project
                filesystem.rm(
                    os.path.join(.project_dir, submodule['path'])
                )
            else:
                raise Exception(f"'{name}' submodule does not exist")
        else:
            raise Exception(f"no gitmodule found at path {gitmodules_path}")

    def add(url, path, link=True):  # type: (str, str, bool) -> None
        """Add submodule to project."""
        # TODO: populate dynamically
        try:
            keypair = Keypair(
                username='git',
                pubkey='id_rsa.pub',
                privkey='id_rsa',
                passphrase='',
            )
            callbacks = RemoteCallbacks(credentials=keypair)
            # XXX: not actually working
            repo().add_submodule(
                url=url, path=path, link=link, callbacks=callbacks
            )
            # repo().index.commit(f'Added {module} submodule')
        except Exception as err:
            print(f"{err}: unable to retrieve submodule")

    def update(name=None):  # type: (Optional[str]) -> None
        """Update submodule within project."""
        if name:
            sm = repo().submodule(name)
            sm.update(recursive=True, init=True)
        else:
            repo().submodule_update(recursive=False)
