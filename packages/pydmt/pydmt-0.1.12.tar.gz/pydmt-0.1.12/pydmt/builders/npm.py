"""
This module installs npm packages
"""


import subprocess

from pydmt.utils.filesystem import unlink_files, mkdir_touch

from pydmt.builders.one_source_one_target import OneSourceOneTarget


class Installer(OneSourceOneTarget):
    def build(self) -> None:
        unlink_files(self.target)
        args = [
            'npm',
            'install',
            '--quiet',
            '--silent',
        ]
        subprocess.check_call(args)
        mkdir_touch(self.target)
