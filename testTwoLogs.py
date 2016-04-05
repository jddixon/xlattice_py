#!/usr/bin/python3

# testTwoLogs.py

import hashlib
import os
import re
import shutil
import sys
import time
import unittest
from xlattice.ftLog import LogMgr
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so


class TestTwoLogs (unittest.TestCase):

    def setUp(self):
        now = time.time()

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################

    def testWithSingleMessage(self):

        if os.path.exists('./logs'):
            shutil.rmtree('./logs')

        # -- open ---------------------------------------------------
        def showLogHandle(h):
            print("HANDLE: %s as %d writing to %s" % (h._baseName,
                                                      h._lfd,
                                                      h._logFile,
                                                      ))
        mgr = LogMgr('logs')
        fooLog = mgr.open('foo')
        fooLog.log('oh hello, foo')
        # showLogHandle(fooLog)                       # DEBUG

        barLog = mgr.open('bar')
        barLog.log('oh hello, bar')
        # showLogHandle(barLog)                       # DEBUG

        # print("TEST_TWO: closing")
        sys.stdout.flush()

        # -- close --------------------------------------------------
        mgr.close()

        # -- test our expectations ----------------------------------
        expectedLogFile = 'logs/foo.log'
        self.assertEqual(expectedLogFile, fooLog.logFileName)
        self.assertTrue(os.path.exists(expectedLogFile))
        with open(expectedLogFile, 'r') as f:
            contents = f.read()
        contents = contents.strip()
        self.assertTrue(contents.endswith('oh hello, foo'))  # END FOO

        if barLog:
            expectedLogFile = 'logs/bar.log'
            self.assertEqual(expectedLogFile, barLog.logFileName)
            self.assertTrue(os.path.exists(expectedLogFile))
            with open(expectedLogFile, 'r') as f:
                contents = f.read()
            contents = contents.strip()
            self.assertTrue(contents.endswith('oh hello, bar'))  # END BAR

if __name__ == '__main__':
    unittest.main()
