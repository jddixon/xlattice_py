#!/usr/bin/env python3

# dev/py/xlattice_py/testULock.py

import os
import unittest

import rnglib
from xlattice import u


"""
We are testing three functions:
    lock = u.ULock(pathToU)
    lock.getLock()
    lock.releaseLock()
"""

U_PATH = 'myU1'


class TestULock (unittest.TestCase):

    def setUp(self):
        if not os.path.exists(U_PATH):
            os.mkdir(U_PATH)
        lock = u.ULock(U_PATH)
        if os.path.exists(lock.lockFile):
            os.remove(lock.lockFile)

    def tearDown(self):
        pass

    # actual unit tests #############################################
    def testConstructor(self):
        """ we are testing lock = u.ULock(pathToU) """
        lock = u.ULock(U_PATH)
        self.assertTrue(lock is not None)
        lockDir = lock.lockDir
        lockFile = lock.lockFile
        pid = lock.pid
        self.assertTrue(os.path.exists(lockDir))
        self.assertFalse(os.path.exists(lockFile))
        self.assertEqual(pid, os.getpid())

    def testGetLock(self):
        """ we are testing lock.getLock() """
        lock = u.ULock(U_PATH)
        success = lock.getLock()
        self.assertTrue(success)
        lockFile = lock.lockFile
        pid = lock.pid
        self.assertTrue(os.path.exists(lockFile))
        with open(lockFile, 'r') as f:
            lockData = f.read()
        self.assertEqual(lockData, str(pid))

        # test that attempt to get second lock fails
        lock2 = u.ULock(U_PATH)
        self.assertFalse(lock2.getLock())
        lock2.releaseLock()

        lock.releaseLock()

    def testReleaseLock(self):
        """ we are testing lock.releaseLock() """
        lock = u.ULock(U_PATH)
        self.assertTrue(lock.getLock(True))
        lockFile = lock.lockFile
        lock.releaseLock()
        # XXX relies on implementation knowledge
        self.assertFalse(os.path.exists(lockFile))

        lock2 = u.ULock(U_PATH)
        self.assertTrue(lock2.getLock())
        lock2.releaseLock()

if __name__ == '__main__':
    unittest.main()
