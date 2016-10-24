#!/usr/bin/env python3

# testTwoLogs.py

import hashlib
import os
import re
import shutil
import sys
import time
import unittest
from xlattice.ftlog import LogMgr
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so


class TestTwoLogs (unittest.TestCase):

    def setUp(self):
        now = time.time()

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def test_with_single_message(self):

        if os.path.exists('./logs'):
            shutil.rmtree('./logs')

        # -- open ---------------------------------------------------
        def show_log_handle(handle):
            print("HANDLE: %s as %d writing to %s" % (handle.base_name,
                                                      handle.lfd,
                                                      handle.logFile,
                                                      ))
        mgr = LogMgr('logs')
        foo_log = mgr.open('foo')
        foo_log.log('oh hello, foo')
        # showLogHandle(fooLog)                       # DEBUG

        bar_log = mgr.open('bar')
        bar_log.log('oh hello, bar')
        # showLogHandle(barLog)                       # DEBUG

        # print("TEST_TWO: closing")
        sys.stdout.flush()

        # -- close --------------------------------------------------
        mgr.close()

        # -- test our expectations ----------------------------------
        expected_log_file = 'logs/foo.log'
        self.assertEqual(expected_log_file, foo_log.log_file_name)
        self.assertTrue(os.path.exists(expected_log_file))
        with open(expected_log_file, 'r') as file:
            contents = file.read()
        contents = contents.strip()
        self.assertTrue(contents.endswith('oh hello, foo'))  # END FOO

        if bar_log:
            expected_log_file = 'logs/bar.log'
            self.assertEqual(expected_log_file, bar_log.log_file_name)
            self.assertTrue(os.path.exists(expected_log_file))
            with open(expected_log_file, 'r') as file:
                contents = file.read()
            contents = contents.strip()
            self.assertTrue(contents.endswith('oh hello, bar'))  # END BAR

if __name__ == '__main__':
    unittest.main()