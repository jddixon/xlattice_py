#!/usr/bin/python3

# testProcLock.py

import hashlib
import os
import re
import time
import unittest
import sys
from rnglib import SimpleRNG
from xlattice.procLock import ProcLock
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so


class TestProcLock (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################
    def testFunctions(self):
        """
        Verify that a lock file is created under /tmp/ and that the
        current PID is written to it.  There should be no errors.
        Verify that the lock file has been removed by the unlock()
        operation.
        """
        try:
            myPID = os.getpid()
            mgr = ProcLock('foo')

            self.assertEqual('foo', mgr.pgmName)
            self.assertEqual(myPID, mgr.pid)
            # XXX bad practice wiring in location
            self.assertEqual('/tmp/run/foo.pid', mgr.lockFileName)
            self.assertTrue(os.path.exists(mgr.lockFileName))
            with open(mgr.lockFileName, 'r') as f:
                pidInFile = f.read()
            self.assertEqual(str(myPID), pidInFile)

            # DEBUG
            print("lock file is %s" % mgr.lockFileName)
            print("  pic in file is %s" % pidInFile)
            # END

        except Exception as e:
            self.fail("unexpected exception %s" % e)
        finally:
            mgr.unlock()
        self.assertFalse(os.path.exists(mgr.lockFileName))

if __name__ == '__main__':
    unittest.main()
