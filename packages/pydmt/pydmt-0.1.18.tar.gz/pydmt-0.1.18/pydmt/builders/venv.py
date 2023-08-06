"""
This module build python virtual envrionments
"""


import os
import shutil
from typing import List, Generator, Tuple
import subprocess

from pydmt.api.builder import Builder, Node, SourceFile, TargetFolder
from pydmt.utils.filesystem import files_under_folder
from pydmt.utils.digest import sha1_file

from pydmt.configs import ConfigOutput

SOURCE_FILE = "config/python.py"
TARGET_FOLDER = ".venv/default"


class BuilderVenv(Builder):
    """
    This is a review of how to build a python virtual environment:
    # create the virtualenv
    virtualenv [folder]
    # activate it
    source [folder]/bin/activate
    # install package
    pip install -r requirements.txt
    """
    def __init__(self):
        # pylint: disable=useless-super-delegation
        super().__init__()

    def get_sources(self) -> List[Node]:
        file_list = [SourceFile(SOURCE_FILE)]
        return file_list

    def get_targets(self) -> List[Node]:
        return [TargetFolder(TARGET_FOLDER)]

    def build(self) -> None:
        if os.path.isdir(TARGET_FOLDER):
            shutil.rmtree(TARGET_FOLDER)
        args = [
            "virtualenv",
            TARGET_FOLDER,
        ]
        if ConfigOutput.verbose:
            subprocess.check_call(args)
        else:
            subprocess.check_call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        args = [
            "venv-run",
            "--venv",
            ".venv/default",
            "--",
            "pip",
            "install",
        ]
        # pylint: disable=import-outside-toplevel
        import config.python
        # pylint: disable=no-member
        args.extend(config.python.test_requires)
        args.extend(config.python.run_requires)
        args.extend(config.python.install_requires)
        args.extend(config.python.setup_requires)
        args.extend(config.python.dev_requires)
        subprocess.check_call(args)

    def yield_results(self) -> Generator[Tuple[str, str], None, None]:
        for x in files_under_folder(TARGET_FOLDER):
            yield sha1_file(x), x
