# xlattice_py/xlattice/lfs

# import errno
import os
import warnings

__all__ = ['mkdir_p', 'touch', ]


def mkdir_p(path, mode=0o777):
    # DROP ON REACHING v1.7 *****************************************
    warnings.warn("mkdir_p deprecated", DeprecationWarning)
    # Python 3
    os.makedirs(path, mode, exist_ok=True)


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)
