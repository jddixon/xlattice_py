#!/usr/bin/env python3

# xlattice_py/testLogMgr.py

import hashlib
import os
import re
import shutil
import time
import unittest
import sys
from xlattice.ftlog import LogMgr
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so


class TestLogMgr(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################
    def test_just_open_and_close(self):
        if os.path.exists('./logs'):
            shutil.rmtree('./logs')
        mgr = LogMgr('logs')
        logger = mgr.open('foo')
        self.assertIsNotNone(logger)
        # print "XXX NO MESSAGES XXX"
        expected_log_file = 'logs/foo.log'
        self.assertEqual(expected_log_file, logger.log_file_name)
        # we don't provide any way to close individual logs
        mgr.close()

        contents = None
        with open(expected_log_file, 'r') as file:
            contents = file.read()
        if contents:
            contents = contents.strip()
            self.assertEqual(0, len(contents))

    def test_with_single_message(self):
        if os.path.exists('./logs'):
            shutil.rmtree('./logs')
        mgr = LogMgr('logs')
        logger = mgr.open('foo')
        logger.log('oh hello')
        # can't test this after logger closed - because object destroyes
        expected_log_file = 'logs/foo.log'
        self.assertEqual(expected_log_file, logger.log_file_name)
        mgr.close()

        self.assertTrue(os.path.exists(expected_log_file))
        with open(expected_log_file, 'r') as file:
            contents = file.read()
        contents = contents.strip()
        self.assertTrue(contents.endswith('oh hello'))    # GEEP

    def test_more_essages(self):
        if os.path.exists('./logs'):
            shutil.rmtree('./logs')
        mgr = LogMgr('logs')
        logger = mgr.open('bar')
        msg = ''
        msg += logger.log("this is gibberish ending in uhm lots of stuff and A")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and B")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and C")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and D")
        expected_log_file = 'logs/bar.log'
        self.assertEqual(expected_log_file, logger._log_file)
        mgr.close()

        self.assertTrue(os.path.exists(expected_log_file))
        with open(expected_log_file, 'r') as file:
            contents = file.read()
        self.assertEqual(msg, contents)          # END

    def test_messages_with_sleeps(self):
        # The presence of a time.sleep() _anywhere_ in the method used
        # to cause a segfault
        if os.path.exists('./logs'):
            shutil.rmtree('./logs')
        mgr = LogMgr('logs')
        logger = mgr.open('baz')
        msg = ''
        msg += logger.log("this is gibberish ending in uhm lots of stuff and A")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and B")
        time.sleep(0.2)
        msg += logger.log("this is gibberish ending in uhm lots of stuff and C")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and D")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and E")
        time.sleep(0.2)
        msg += logger.log("this is gibberish ending in uhm lots of stuff and F")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and G")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and H")
        time.sleep(0.2)
        expected_log_file = 'logs/baz.log'
        self.assertEqual(expected_log_file, logger._log_file)
        mgr.close()

        self.assertTrue(os.path.exists(expected_log_file))
        with open(expected_log_file, 'r') as file:
            contents = file.read()
        self.assertEqual(msg, contents)      # FOOFOO

if __name__ == '__main__':
    unittest.main()
