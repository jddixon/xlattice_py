# xlattice_py/xlattice/procLock.py

import os
import re
import subprocess
import sys
import time
from cFTLogForPy import (initCFTLogger, openCFTLog, logMsg, closeCFTLogger)

__all__ = ['ProcLockMgr', ]

# CONSTANTS #########################################################

PS = '/bin/ps'
SH = '/bin/sh'

# -------------------------------------------------------------------


class ProcLockMgr(object):

    def __init__(self, pgmName, pidDir='/tmp/run'):
        self._pid = os.getpid()
        self._pgmName = pgmName
        self._pidFile = os.path.join(pidDir, pgmName + '.pid')

        # If the pid file exists, extract the process ID.  If that
        # pid is running, we are done, there is nothing else to do.
        # Otherwise we will overwrite the PID file.
        if os.path.exists(self._pidFile):
            pidRunning = ProcLockMgr.readOneLineFile(self._pidFile)
            whether = ProcLockMgr.isProcessRunning(pidRunning)
            if(whether):
                sys.exit()
        if not os.path.exists(pidDir):
            os.makedirs(pidDir)         # the run directory is created
        ProcLockMgr.writeOneLineFile(self._pidFile, str(self._pid))

    @property
    def pid(self):
        return self._pid

    @property
    def pgmName(self):
        return self._pgmName

    @property
    def lockFileName(self):
        return self._pidFile

    @staticmethod
    def isProcessRunning(pid):
        pidStr = str(pid)
        ret = False
        pat = re.compile('^(\w+)\s+(\d+)')
        p = subprocess.Popen([PS, 'waux'], stdout=subprocess.PIPE)
        if p:
            while (True):
                line = p.stdout.readline()
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

    def removePIDFile(self):
        if os.path.exists(self._pidFile):
            os.remove(self._pidFile)

    def unlock(self):
        self.removePIDFile()

    # UTILITY FUNCTIONS
    @staticmethod
    def readOneLineFile(name):
        with open(name, "r") as f:
            return f.readline().strip()

    @staticmethod
    def readOneLineFileIf(fileName, default):
        ret = default
        if (os.path.exists(fileName)):
            ret = ProcLockMgr.readOneLineFile(fileName)
        return ret

    # EXCEPTIONS are ignored
    @staticmethod
    def writeOneLineFile(fileName, value):
        with open(fileName, 'w') as f:
            f.write(value)
