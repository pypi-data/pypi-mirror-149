import shutil

from pydmt.builders.one_source_one_target import OneSourceOneTarget


class Copy(OneSourceOneTarget):
    def build(self):
        shutil.copy(self.source, self.target)
