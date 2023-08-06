import sys
from cbutil import Path
from .path import *

__all__ = ['path']

path = make_path_info(Path(sys.argv[0]).prnt)


