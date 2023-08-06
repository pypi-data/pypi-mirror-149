from typing import *
import dataclasses
from dataclasses import dataclass
import sys

from cbutil import Path
from .rand import *

__all__ = ['make_path_info']


def make_path_info(r: Union[Path, str]):
    @dataclass
    class _path:
        root: Path = Path(r)
        core: Path = root/'core'      # for read-only data
        data: Path = root/'data'   # for persistent data
        cache: Path = root/'cache'
        tmp: Path = root/'tmp'

        messey: Path = tmp/'messey'  # for any temp files

        def clean_tmp(self):
            self.tmp.remove_sons()

        def make_tmp(self, suffix='', prefix=''):
            return self.messey / (prefix + make_id_str() + suffix)
        
        def create_path(self):
            for p in dataclasses.astuple(self):
                p: Path
                p.mkdir()
            
    path = _path()

    return path
