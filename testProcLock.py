#!/usr/bin/python3

# testProcLock.py

import hashlib
import os
import re
import time
import unittest
import sys
from rnglib import SimpleRNG
from xlattice.procLock import ProcLockMgr
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so


class TestProcLockMgr (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################
    def testFunctions(self):
        myPID = os.getpid()
        mgr = ProcLockMgr('foo')

        self.assertEqual('foo', mgr.pgmName)
        self.assertEqual(myPID, mgr.pid)
        # XXX bad practice wiring in location
        self.assertEqual('/tmp/run/foo.pid', mgr.lockFileName)
        self.assertTrue(os.path.exists(mgr.lockFileName))
        with open(mgr.lockFileName, 'r') as f:
            pidInFile = f.read()
        self.assertEqual(str(myPID), pidInFile)

        mgr.unlock()
        self.assertFalse(os.path.exists(mgr.lockFileName))

if __name__ == '__main__':
    unittest.main()
