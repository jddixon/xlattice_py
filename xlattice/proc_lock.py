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
        self._pgmName = pgm_name
        self._pidFile = os.path.join(pid_dir, pgm_name + '.pid')

        # If the pid file exists, extract the process ID.  If that
        # pid is running, we are done, there is nothing else to do.
        # Otherwise we will overwrite the PID file.
        if os.path.exists(self._pidFile):
            pidRunning = ProcLock.read_one_line_file(self._pidFile)
            whether = ProcLock.is_process_running(pidRunning)
            if(whether):
                sys.exit()
        if not os.path.exists(pid_dir):
            os.makedirs(pid_dir)         # the run directory is created
        ProcLock.writeOneLineFile(self._pidFile, str(self._pid))

    @property
    def pid(self):
        return self._pid

    @property
    def pgm_name(self):
        return self._pgmName

    @property
    def lockFileName(self):
        return self._pidFile

    @staticmethod
    def is_process_running(pid):
        pidStr = str(pid)
        ret = False
        pat = re.compile('^(\w+)\s+(\d+)')
        p = subprocess.Popen([PS, 'waux'], stdout=subprocess.PIPE)
        if p:
            while (True):
                # XXX
                line = p.stdout.read().decode('utf-8')
                if (line == ''):
                    break
                m = pat.match(line)
                if (m):
                    pid = m.group(2)
                    if(pid == pidStr):
                        ret = True
                        break
            p.stdout.close()
        return ret

    def remove_pid_file(self):
        if os.path.exists(self._pidFile):
            os.remove(self._pidFile)

    def unlock(self):
        self.remove_pid_file()

    # UTILITY FUNCTIONS
    @staticmethod
    def read_one_line_file(name):
        with open(name, "rb") as file:
            data = file.read()
            return data.decode('utf-8').strip()

    @staticmethod
    def readOneLineFileIf(fileName, default):
        ret = default
        if (os.path.exists(fileName)):
            ret = ProcLock.read_one_line_file(fileName)
        return ret

    # possible EXCEPTIONS are ignored
    @staticmethod
    def writeOneLineFile(fileName, value):
        with open(fileName, 'wb') as file:
            file.write(value.encode('utf-8'))
