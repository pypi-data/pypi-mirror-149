"""
This is a module that will install OS packages for you.
"""


from typing import List
import subprocess
import os

from pydmt.utils.filesystem import unlink_files, mkdir_touch
from pydmt.configs import ConfigSudo

from pydmt.builders.one_source_one_target import OneSourceOneTarget


class Installer(OneSourceOneTarget):
    def __init__(self, source: str, target: str, packages: List[str]):
        super().__init__(source, target)
        self.packages = packages

    def build(self) -> None:
        unlink_files(self.target)
        os.environ['DEBIAN_FRONTEND'] = 'noninteractive'
        args = []
        if ConfigSudo.sudo:
            args.append("sudo")
        args.extend([
            'apt-get',
            '--yes',
            '--quiet',
            'install',
        ])
        args.extend(self.packages)
        subprocess.check_call(args)
        mkdir_touch(self.target)
