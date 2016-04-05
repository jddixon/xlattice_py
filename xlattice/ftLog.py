# xlattice_py/xlattice/ftLog.py

import os
import sys
import time

from cFTLogForPy import (initCFTLogger, openCFTLog, logMsg, closeCFTLogger,
                         )

__all__ = ['LogEntry',
           'ActualLog', 'LogMgr',
           ]

# The first line of a chained log is a LogEntry pointing back to
# the previous chunk of the log; its key is the content key of that
# log in U.

# See upax_go/entry.go and entry_test.go


class LogEntry(object):

    def __init__(self,
                 t,              # integer timestamp, either 32 or 64 bits
                 key,            # content key, 20 or 32 bytes
                 owner,          # nodeID, 20 or 32 bytes
                 length,         # uint32 length of content, octets
                 src,            # aka 'by'
                 path):          # path relative to project root

        self._t = t
        self._key = key
        self._owner = owner,
        self._length = length
        self._src = src
        self._path = path

    @property
    def t(self): return self._t

    @property
    def key(self): return self._key

    @property
    def owner(self): return self._owner

    @property
    def length(self): return self._length

    @property
    def src(self): return self._src

    @property
    def path(self): return self._path

    def __eq__(self, other):
        if not isinstance(other, LogEntry):
            return False
        return self._t == other._t and \
            self._key == other._key and \
            self._owner == other._owner and \
            self._length == other._length and \
            self._src == other._src and \
            self._path == other._path


# -------------------------------------------------------------------
class ActualLog(object):
    """ maintains information about each open log """

    def __init__(self, baseName, mgr):
        """
        Creates a new access log. The caller guarantees that the
        base name is unique.
        """
        # __slots__ = { '__baseName',
        self._baseName = baseName
        self._mgr = mgr
        self._logFile = os.path.join(mgr.logDir, baseName + '.log')
        self._lfd = None

        # we pass the full path name
        self.nameCopy = self._logFile.strip()   # should copy the string
        # DEBUG
        #print("trying to open log with path '%s'" % self.nameCopy)
        # END
        lfd = openCFTLog(self.nameCopy)
        if lfd < 0:
            raise RuntimeError("ERROR: initCFTLogger returns %d", lfd)
        else:
            # DEBUG
            # print("opened %s successfully with lfd %d" % (self._logFile, lfd))
            # END
            self._lfd = lfd

    def log(self, msg):
        now = time.localtime()
        date = time.strftime('%Y-%m-%d', now)
        hours = time.strftime('%H:%M:%S', now)
        text = '%s %s %s\n' % (date, hours, msg)
        # note that this is a tuple
        status = logMsg(self._lfd, text)
        # XXX handle possible errors

#       # DEBUG Python3-style
#       print ("message is: '%s'",  text)
#       # END
        return text

    @property
    def logFileName(self):
        return self.nameCopy


class LogMgr(object):

    def __init__(self, logDir='logs'):
        """
        This is a MAJOR CHANGE in the interface.
        """

        # __slots__ = { }

        # a map indexed by the base name of the log
        self._logMap = {}
        self._logDir = logDir

        # THIS IS A PARTIAL FIX: the above assumes that all logs
        # share the same directory
        status = initCFTLogger()

    def open(self, baseName):
        if baseName in self._logMap:
            raise ValueError('log named %s already exists' % baseName)
        logHandle = ActualLog(baseName, self)
        if logHandle:
            self._logMap[baseName] = logHandle
            # DEBUG
            # print("logHandle for %s is %s" % (baseName, str(logHandle)))
            # END
            return logHandle

    def close(self):
        """closes all log files """
        self._logMap = {}
        # print("BRANCHING TO closeClogger()") ; sys.stdout.flush();
        return closeCFTLogger(None)

    @property
    def logDir(self):
        return self._logDir
