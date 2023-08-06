"""
This module build python virtual envrionments
"""


import os
import shutil

from pydmt.utils.filesystem import mkdir_touch
from pydmt.utils.subprocess import check_call
from pydmt.utils.python import collect_reqs, get_install_args

from pydmt.api.one_source_one_target import OneSourceOneTarget

SOURCE_FILE = "config/python.py"
TARGET_FOLDER = ".venv/default"


class BuilderVenv(OneSourceOneTarget):
    """
    This is a review of how to build a python virtual environment:
    # create the virtualenv
    virtualenv [folder]
    # activate it
    source [folder]/bin/activate
    # install package
    pip install -r requirements.txt
    """
    def build(self) -> None:
        if os.path.isdir(TARGET_FOLDER):
            shutil.rmtree(TARGET_FOLDER)
        args = [
            "virtualenv",
            TARGET_FOLDER,
        ]
        check_call(args)
        args = [
            "venv-run",
            "--venv",
            ".venv/default",
            "--",
        ]
        get_install_args(args)
        if collect_reqs(args):
            check_call(args)
        mkdir_touch(self.target)
