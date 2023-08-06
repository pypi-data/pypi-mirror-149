import sys
from cbutil import Path

import rmgr.config as config
from .path import make_path_info

__all__ = ['init_rmgr']


def init_rmgr(r:Path = None):
    '''
    initialize module, always call this function before import any other submodules
    r : root path
    '''
    if r is None:
        r = Path(sys.argv[0]).prnt
    path = make_path_info(r)
    path.create_path()
    config.path = path


