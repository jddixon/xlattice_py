#!/usr/bin/env python3
# testProcLock.py

""" Test ProcLock functionality. """

import os
import unittest
import sys
from rnglib import SimpleRNG
from xlattice.proc_lock import ProcLock, ProcLockError
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so


class TestProcLock(unittest.TestCase):

    """ Test ProcLock functionality. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_fail(self):
        try:
            my_pid = os.getpid()
            mgr = ProcLock('foo')
            self.assertEqual('foo', mgr.pgm_name)
            self.assertEqual(my_pid, mgr.pid)
            self.assertEqual('/tmp/run/foo.pid', mgr.lock_file_name)
            self.assertTrue(os.path.exists(mgr.lock_file_name))
            with open(mgr.lock_file_name, 'r') as file:
                pid_in_file = file.read()
            self.assertEqual(str(my_pid), pid_in_file)

            mgr2 = None
            try:
                mgr2 = ProcLock('foo')
                self.fail('successfully got second lock on locked file')
            except ProcLockError:
                pass
            finally:
                if mgr2:
                    mgr2.unlock()
        finally:
            mgr.unlock()

    def test_should_succeed(self):
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
            self.assertEqual('/tmp/run/foo.pid', mgr.lock_file_name)
            self.assertTrue(os.path.exists(mgr.lock_file_name))
            with open(mgr.lock_file_name, 'r') as file:
                pid_in_file = file.read()
            self.assertEqual(str(my_pid), pid_in_file)

        except ProcLockError as exc:
            self.fail("unexpected ProcLockError %s" % exc)
        finally:
            mgr.unlock()
        self.assertFalse(os.path.exists(mgr.lock_file_name))

if __name__ == '__main__':
    unittest.main()
