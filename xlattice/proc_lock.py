# xlattice_py/xlattice/procLock.py

""" Simplistic lock on program name. """

import os
import re
import subprocess
import sys

__all__ = ['ProcLock', 'ProcLockError']

PS = '/bin/ps'
SH = '/bin/sh'


class ProcLockError(RuntimeError):
    pass


class ProcLock(object):
    """
    Simplistic lock on program name.

    Normal use:

        try:
            mgr = ProcLock(PGM_NAME)
            # invoke program body
            # ...
            mgr.unlock()
        except ProcLockError:
            print("can't get lock on %s" % PGM_NAME)
            sys.exit(1)

    More elaborate handler can wait a few seconds and try again,
    perhaps for some number of iterations.

    """

    def __init__(self, pgm_name, pid_dir='/tmp/run'):
        self._pid = os.getpid()
        self._pgm_name = pgm_name
        self._pid_file = os.path.join(pid_dir, pgm_name + '.pid')

        # XXX RACE CONDITION
        # If the pid file exists, extract the process ID.  If that
        # pid is running, we are done, there is nothing else to do.
        # Otherwise we will overwrite the PID file.
        if os.path.exists(self._pid_file):
            pid_running = ProcLock._read_one_line_file(self._pid_file)
            if ProcLock.is_process_running(pid_running):
                raise ProcLockError("can't get lock on %s" % self._pgm_name)
        os.makedirs(pid_dir, exist_ok=True)  # the run directory is created
        ProcLock._write_one_line_file(self._pid_file, str(self._pid))

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
        """
        Return whether process whose PID in string form is pid is running.
        """
        return os.path.exists("/proc/%s" % pid)

    def remove_pid_file(self):
        if os.path.exists(self._pid_file):
            os.remove(self._pid_file)

    def unlock(self):
        self.remove_pid_file()

    # UTILITY FUNCTIONS
    @staticmethod
    def _read_one_line_file(name):
        with open(name, "rb") as file:
            data = file.read()
            return data.decode('utf-8').strip()

    @staticmethod
    def _read_one_line_file_if(file_name, default):
        ret = default
        if os.path.exists(file_name):
            ret = ProcLock._read_one_line_file(file_name)
        return ret

    # possible EXCEPTIONS are ignored
    @staticmethod
    def _write_one_line_file(file_name, value):
        with open(file_name, 'wb') as file:
            file.write(value.encode('utf-8'))
