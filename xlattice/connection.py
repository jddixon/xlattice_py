# xlattice_py/xlattice/connection.py


"""
An XLattice Connection is a relationship between two EndPoints.  In XLattice,
one EndPoint will have an Address on this Node.  The other EndPoint
will have an Address associated with a second Node.  There is always
a transport protocol associated with the connection; both EndPoints
use this same protocol.

Connections are established to allow one or more Messages to be passed
between the Nodes at the two EndPoints.

XXX Connections could be homogeneous or heterogeneous.  In the first
XXX case, each EndPoint would use the same transport.  In the second case,
XXX the heterogeneous Connection, the two EndPoints would use different
XXX transports.

A connection passes through a set of states.  This progress is
irreversible.  Each state has an associated numeric value.  The
order of these values is guaranteed.  That is, UNBOUND is less
than BOUND, which is less than PENDING, and so forth.  Therefore
it is reasonable to test on the relative value of states.

XXX If the Transport is Udp, then it is likely that we will want
XXX to be able to bind and unbind the connection, allowing us to use
XXX it with more than one remote EndPoint.  In this case, the
XXX progression through numbered states would not be irreversible.

If new states are defined, they should adhere to this contract.
That is, the passage of a connection through a sequence of states
must be irreversible, and the numeric value of any later state
must be greater than that associated with any earlier state.

XXX Any application can encrypt data passing over a connection.
XXX Is it reasonable to mandate what follows as part of the
XXX interface?

There may be a secret key associated with the Connection.  This
will be used with a symmetric cipher to encrypt and decrypt
traffic over the Connection.  Such secret keys are negotiated
between the EndPoint Nodes and possibly periodically renegotiated.

Connections exist at various levels of abstraction.  TCP, for
example, is layered on top of IP, and BGP4 on top of TCP.  It is
possible for a connection to be in clear, but used for carrying
encrypted messages at a higher protocol level.  It is equally
possible that data passing over a connection will be encrypted
at more than one level.
"""

from abc import ABCMeta, abstractmethod
from enum import IntEnum


class Connection(metaclass=ABCMeta):
    """ An XLattice Connection between two EndPoints. """

    class State(IntEnum):
        """ Values are ascending and may only be assigned progressively. """

        # neither EndPoint is set
        UNBOUND = 100
        # near EndPoint is set
        BOUND = 200
        # connection to far EndPoint has been requested
        PENDING = 300
        # both EndPoints have been set, connection is established
        CONNECTED = 400
        # connection has been closed
        DISCONNECTED = 500

    @abstractmethod
    def get_state(self):             # -> Connection.State
        """
        Return the current state index.  In the current implementation,
        this is not necessarily reliable, but the actual state index
        is guaranteed to be no less than the value reported.
        """
        pass

    @abstractmethod
    def bind_near_end(self, endp):  # endp an EndPoint     # raises IOException
        """
        Set the near EndPoint of a connection.  If either the
        near or far EndPoint has already been set, this will
        raise an exception.  If successful, the connection's
        state becomes BOUND.

        @param endp the near end
        Raise IOException if either EndPoint already set
        """
        pass

    @abstractmethod
    def bind_far_end(self, endp):  # endp an EndPoint     # raises IOException
        """
        Set the far EndPoint of a connection.  If the near end
        point has NOT been set or if the far EndPoint has already
        been set -- in other words, if the connection is already
        beyond state BOUND -- this will raise an exception.
        If the operation is successful, the connection's state
        becomes either PENDING or CONNECTED.

        XXX The state should become CONNECTED if the far end is on
        XXX the same host and PENDING if it is on a remoted host.

        @param endp the far end
        Raise IOException if near EndPoint not set or far end already set
        """
        pass

    @abstractmethod
    def close(self):                          # raises IOException
        """
        Bring the connection to the DISCONNECTED state.

        Raise IOException if not in appropriate state (if not connected)
        """
        pass

    @abstractmethod
    def is_closed(self):         # -> bool
        """
        This should be considered deprecated.  Test on whether the
        state is DISCONNECTED instead.

        Return whether the connection state is DISCONNECTED.
        """
        pass

    # END POINTS ///////////////////////////////////////////////////
    @abstractmethod
    def get_near_end(self):      # -> EndPoint
        """ Return the near EndPoint of the Connection. """
        pass

    @abstractmethod
    def get_far_end(self):       # -> EndPoint
        """ Return the far EndPoint of the Connection. """
        pass

    # I/O //////////////////////////////////////////////////////////
    @abstractmethod
    def is_blocking(self):       # -> bool
        """ Return whether the Connection is blocking. """
        pass

    # ///////////////////////////////////////////////////////////////////
    # XXX CONFUSION BETWEEN PACKET vs STREAM AND BLOCKING vs NON-BLOCKING
    # ///////////////////////////////////////////////////////////////////
    # non-blocking

    # blocking
    @abstractmethod
    def get_input_stream(self):  # -> InputStream    # raises IOException
        """ Return the InputStream associated with the Connection. """
        pass

    @abstractmethod
    def get_output_stream(self):  # -> OutputStream   # raises IOException
        """ Return the OutputStream associated with the Connection. """
        pass

    # ENCRYPTION ///////////////////////////////////////////////////

    @abstractmethod
    def is_encrypted(self):     # -> bool
        """ Return whether the connection is encrypted. """
        pass

    @abstractmethod
    def negotiate(self, my_key, his_key):
        """
        (Re)negotiate the secret used to encrypt traffic over the
        connection.
        @param myKey  this Node's asymmetric key
        @param hisKey Peer's def key
        """
        pass

    @abstractmethod
    def __eq__(self, other):             # -> bool
        """ Return whether this Connection and the other are equal. """
        return False

    @abstractmethod
    def hashcode(self):              # -> int
        """ Return a smoothly-distributed hashcode for the Connection. """
        pass
