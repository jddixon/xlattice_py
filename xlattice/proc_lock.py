# xlattice_py/xlattice/procLock.py

import os
import re
import subprocess
import sys
import time
from cFTLogForPy import (
    init_cft_logger,
    openCFTLog,
    log_msg,
    close_cft_logger)

__all__ = ['ProcLock', ]

# CONSTANTS #########################################################

PS = '/bin/ps'
SH = '/bin/sh'

# -------------------------------------------------------------------


class ProcLock(object):

    def __init__(self, pgm_name, pid_dir='/tmp/run'):
        self._pid = os.getpid()
        self._pgm_name = pgm_name
        self._pid_file = os.path.join(pid_dir, pgm_name + '.pid')

        # If the pid file exists, extract the process ID.  If that
        # pid is running, we are done, there is nothing else to do.
        # Otherwise we will overwrite the PID file.
        if os.path.exists(self._pid_file):
            pid_running = ProcLock.read_one_line_file(self._pid_file)
            whether = ProcLock.is_process_running(pid_running)
            if(whether):
                sys.exit()
        if not os.path.exists(pid_dir):
            os.makedirs(pid_dir)         # the run directory is created
        ProcLock.writeOneLineFile(self._pid_file, str(self._pid))

    @property
    def pid(self):
        return self._pid

    @property
    def pgm_name(self):
        return self._pgm_name

    @property
    def lock_file_name(self):
        return self._pid_file

    @staticmethod
    def is_process_running(pid):
        pid_str = str(pid)
        ret = False
        pat = re.compile('^(\w+)\s+(\d+)')
        ppp = subprocess.Popen([PS, 'waux'], stdout=subprocess.PIPE)
        if ppp:
            while (True):
                # XXX
                line = ppp.stdout.read().decode('utf-8')
                if (line == ''):
                    break
                match = pat.match(line)
                if (match):
                    pid = match.group(2)
                    if(pid == pid_str):
                        ret = True
                        break
            ppp.stdout.close()
        return ret

    def remove_pid_file(self):
        if os.path.exists(self._pid_file):
            os.remove(self._pid_file)

    def unlock(self):
        self.remove_pid_file()

    # UTILITY FUNCTIONS
    @staticmethod
    def read_one_line_file(name):
        with open(name, "rb") as file:
            data = file.read()
            return data.decode('utf-8').strip()

    @staticmethod
    def readOneLineFileIf(file_name, default):
        ret = default
        if (os.path.exists(file_name)):
            ret = ProcLock.read_one_line_file(file_name)
        return ret

    # possible EXCEPTIONS are ignored
    @staticmethod
    def writeOneLineFile(file_name, value):
        with open(file_name, 'wb') as file:
            file.write(value.encode('utf-8'))
