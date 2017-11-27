# xlattice_py/xlattice/lfs

""" Local file system-related utility functions. """

import os

__all__ = ['touch', ]


def touch(fname, times=None):
    """ Emulate UNIX touch. """

    with open(fname, 'a'):
        os.utime(fname, times)
