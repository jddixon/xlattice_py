# xlattice_py/xlattice/ftLog.py

__all__ = ['LogEntry',
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
