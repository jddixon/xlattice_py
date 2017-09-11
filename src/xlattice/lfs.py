# xlattice_py/xlattice/lfs

import os

__all__ = ['touch', ]


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)
