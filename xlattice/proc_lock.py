# xlattice_py/xlattice/procLock.py

""" Simplistic lock on program name. """

import os

__all__ = ['ProcLock', 'ProcLockError']

PS = '/bin/ps'
SH = '/bin/sh'


class ProcLockError(RuntimeError):
    pass


class ProcLock(object):
    """
    Simplistic lock on path to object being locked.

    Normal use:

        try:
            mgr = ProcLock(PATH_TO_NAME)
            # invoke program body
            # ...
        except ProcLockError:
            print("can't get lock on %s" % PATH_TO_NAME)
            sys.exit(1)
        finall:
            if mgr:
                mgr.unlock()

    More elaborate handler can wait a few seconds and try again,
    perhaps for some number of iterations.

    This implementation assumes a cooperative environment, not a hostile
    one.  Users should lock on absolute paths but the code will work
    with agreed-upon relative paths.  Absolute paths are very much
    preferred.
    """

    def __init__(self, path_to_name, pid_dir='/tmp/run'):
        if path_to_name and path_to_name[0] == '/':
            path_to_name = path_to_name[1:]
        if not path_to_name:
            raise ProcLockError('empty path -- nothing to lock')
        # XXX other checks on path

        self._pid = os.getpid()

        full_path_to_name = os.path.join(pid_dir, path_to_name)

        path_part, delim, _ = full_path_to_name.rpartition('/')
        if delim == '/':
            os.makedirs(path_part, exist_ok=True, mode=0o777)

        self._pid_file = os.path.join(pid_dir, full_path_to_name + '.pid')

        # XXX RACE CONDITION
        # If the pid file exists, extract the process ID.  If that
        # pid is running, we are done, there is nothing else to do.
        # Otherwise we will overwrite the PID file.
        if os.path.exists(self._pid_file):
            pid_running = ProcLock._read_one_line_file(self._pid_file)
            if ProcLock.is_process_running(pid_running):
                raise ProcLockError("can't get lock on %s" % full_path_to_name)
        ProcLock._write_one_line_file(self._pid_file, str(self._pid))
        self._full_path_to_name = full_path_to_name

    @property
    def pid(self):
        """ Return the PID, a 16-bit integer. """
        return self._pid

    @property
    def full_path_to_name(self):
        """ Return the absolute path to the PID file. """
        return self._full_path_to_name

    @property
    def lock_file_name(self):
        """ Return the name of the PID file. """
        return self._pid_file

    @staticmethod
    def is_process_running(pid):
        """
        Return whether process whose PID in string form is pid is running.
        """
        return os.path.exists("/proc/%s" % pid)

    def remove_pid_file(self):
        """ If a PID file exists, remove it. """
        if os.path.exists(self._pid_file):
            os.remove(self._pid_file)

    def unlock(self):
        """ Unlock by removing the PID file. """
        self.remove_pid_file()

    # UTILITY FUNCTIONS
    @staticmethod
    def _read_one_line_file(name):
        """ Read test from a one-line file. """
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
