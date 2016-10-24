#!/usr/bin/env python3

# testProcLock.py

import hashlib
import os
import re
import time
import unittest
import sys
from rnglib import SimpleRNG
from xlattice.proc_lock import ProcLock
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so


class TestProcLock(unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################
    def test_functions(self):
        """
        Verify that a lock file is created under /tmp/ and that the
        current PID is written to it.  There should be no errors.
        Verify that the lock file has been removed by the unlock()
        operation.
        """
        try:
            my_pid = os.getpid()
            mgr = ProcLock('foo')

            self.assertEqual('foo', mgr.pgm_name)
            self.assertEqual(my_pid, mgr.pid)
            # XXX bad practice wiring in location
            self.assertEqual('/tmp/run/foo.pid', mgr.lockFileName)
            self.assertTrue(os.path.exists(mgr.lockFileName))
            with open(mgr.lockFileName, 'r') as file:
                pid_in_file = file.read()
            self.assertEqual(str(my_pid), pid_in_file)

            # DEBUG
            print("lock file is %s" % mgr.lockFileName)
            print("  pid in file is %s" % pid_in_file)
            # END

        except Exception as exc:
            self.fail("unexpected exception %s" % exc)
        finally:
            mgr.unlock()
        self.assertFalse(os.path.exists(mgr.lockFileName))

if __name__ == '__main__':
    unittest.main()