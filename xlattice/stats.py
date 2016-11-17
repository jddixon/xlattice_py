#!/usr/bin/python3

# ~/dev/py/xlattice_py/xlattice/stats.py

import os
import re
import shutil
import stat
import sys
from argparse import ArgumentParser

from xlattice import (__version__, __version_date__, QQQ)
from xlattice.u import (file_sha1hex, UDir,)

try:
    from os.scandir import scandir
except ImportError:
    from scandir import scandir

###############################
# XXX assumes usingSHA == True
###############################

HEX2_PAT = '^[0-9a-fA-F][0-9a-fA-F]$'
HEX2_RE = re.compile(HEX2_PAT)

SHA1_PAT = '^[0-9a-fA-F]{40}$'
SHA1_RE = re.compile(SHA1_PAT)


class UStats:

    def __init__(self):
        self._dir_struc = UDir.DIR_FLAT
        self._using_sha = False

        self._sub_dir_count = 0
        self._sub_sub_dir_count = 0
        self._leaf_count = 0
        self._odd_count = 0
        self._has_l = False
        self._has_node_id = False
        self._min_leaf_bytes = sys.maxsize
        self._max_leaf_bytes = 0

        self._unexpected_at_top = []

    @property
    def dir_struc(self): return self._dir_struc   # an int

    @property
    def using_sha(self): return self._using_sha

    @property
    def subdir_count(self):
        return self._sub_dir_count

    @property
    def sub_subdir_count(self):
        return self._sub_sub_dir_count

    @property
    def leaf_count(self):
        return self._leaf_count

    @property
    def odd_count(self):
        return self._odd_count

    @property
    def has_l(self):
        return self._has_l

    @property
    def has_node_id(self):
        return self._has_node_id

    @property
    def min_leaf_bytes(self):
        return self._min_leaf_bytes

    @property
    def max_leaf_bytes(self):
        return self._max_leaf_bytes

    @property
    def unexpected_at_top(self):
        return self._unexpected_at_top


def scan_leaf_dir(path_to_dir, obj):
    # DEBUG
    # #print("    scanning leaf directory %s" % pathToDir)
    # END
    file_count = 0
    odd_count = 0

    for entry in scandir(path_to_dir):
        # DEBUG
        #print("      leaf file: %s" % entry.name)
        # END
        if entry.is_symlink():
            # DEBUG
            # print("          SYM LINK")
            # eND
            continue
        name = entry.name
        match = SHA1_RE.match(name)
        if match:
            # DEBUG
            #print("      MATCH")
            # END
            file_count = file_count + 1
            size = entry.stat().st_size
            # DEBUG
            # print("      SIZE = %9d" % size)
            # END
            if size < obj.min_leaf_bytes:
                obj._minLeafBytes = size
            if size > obj.max_leaf_bytes:
                obj._max_leaf_bytes = size
        else:
            odd_count = odd_count + 1
    obj._leaf_count += file_count
    obj._odd_count += odd_count


def collect_stats(u_path, out_path, verbose):
    """
    Drop-in replacement for collect_stats(), using scandir instead of listdir.
    """

    stats = UStats()        # we will return this

    # XXX outPath IS NOT USED
    if out_path:
        os.makedirs(out_path, exist_ok=True)
    # END NOT USED

    u_dir = UDir.discover(u_path)
    stats._using_sha = u_dir.using_sha
    stats._dir_struc = u_dir.dir_struc

    # upper-level files / subdirectories
    for top_entry in scandir(u_path):
        top_file = top_entry.name

        # -- upper-level files ----------------------------------------

        # At this level we expect 00-ff, tmp/ and in/ subdirectories
        # plus the files L and possibly nodeID.

        match = HEX2_RE.match(top_file)
        if match:

            # -- upper-level directories ------------------------------

            stats._sub_dir_count += 1
            path_to_sub_dir = os.path.join(u_path, top_file)
            # DEBUG
            # print("SUBDIR: %s" % path_to_sub_dir)
            # END
            for mid_entry in scandir(path_to_sub_dir):
                mid_file = mid_entry.name
                match2 = HEX2_RE.match(mid_file)
                if match2:

                    stats._sub_sub_dir_count += 1
                    path_to_sub_sub_dir = os.path.join(
                        path_to_sub_dir, mid_file)
                    # DEBUG
                    # print("  SUBSUBDIR: %s" % path_to_sub_sub_dir)
                    # END
                    # XXX WAS MAJOR ERROR
                    # for sub_sub_file in os.listdir(path_to_sub_sub_dir):
                    scan_leaf_dir(path_to_sub_sub_dir, stats)

                # -- other upper-level files --------------------------
                else:
                    path_to_oddity = os.path.join(path_to_sub_dir, mid_file)
                    print("unexpected: %s" % path_to_oddity)
                    stats._odd_count += 1

        #-- other upper-level files -----------------------------------

        else:
            if top_file == 'L':
                stats._has_l = True
            elif top_file == 'node_id':
                stats._has_node_id = True
            elif top_file in ['in', 'tmp']:
                # DEBUG
                # print("TOP LEVEL OTHER DIR: %s" % topFile)
                path_to_dir = os.path.join(u_path, top_file)
                scan_leaf_dir(path_to_dir, stats)
            else:
                path_to_oddity = os.path.join(u_path, top_file)
                stats._unexpected_at_top.append(path_to_oddity)
                stats._odd_count += 1

    return stats
