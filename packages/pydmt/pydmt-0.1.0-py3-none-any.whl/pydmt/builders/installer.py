"""
This is a module that will install OS packages for you.
"""


from typing import List
import subprocess

from pydmt.utils.filesystem import unlink_files, mkdir_touch

from pydmt.builders.one_source_one_target import OneSourceOneTarget


class Installer(OneSourceOneTarget):
    def __init__(self, source: str, target: str, packages: List[str]):
        super().__init__(source, target)
        self.packages = packages

    def build(self) -> None:
        unlink_files(self.target)
        # xargs -a [file with list of packages] sudo apt-get -y install > /dev/null
        args = [
            'sudo',
            'apt-get',
            'install',
        ]
        args.extend(self.packages)
        subprocess.check_call(args)
        mkdir_touch(self.target)
