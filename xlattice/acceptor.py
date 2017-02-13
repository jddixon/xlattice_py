# xlattice_py/xlattice/acceptor.py

"""
The XLattice Acceptor.

An Acceptor is used by a Node or Peer to accept connection requests.
It is an advertisement for a service within a Overlay, that is,
within a given address space and using a particular transport
protocol.

An Acceptor is an abstraction of a TCP/IP ServerSocket.  It is a
single EndPoint whose Address may be well known.  Other entities on
the network send messages to the Acceptor in order to establish
Connections.  The Acceptor may in some cases NOT be one of the
EndPoints involved in the new Connection; the Connection might
be between the requesting remote EndPoint and a new, ephemeral
local EndPoint.

The transport protocol understood by the Acceptor need not be
the same as the transport protocol of Connections created.  That is,
the new Connection need not be in the same Overlay as the Acceptor.

"""

from abc import ABCMeta, abstractmethod


class Acceptor(ABCMeta):
    """ Basic functionality of the XLattice Acceptor. """

    @abstractmethod
    def accept(cls):            # -> Conneaction    # throws IOException
        """ Establish a Connection on the Acceptor. """
        pass

    @abstractmethod
    def close(cls):                                 # throws IOException
        """ Close the Acceptor, an irrevocable step. """
        pass

    @abstractmethod
    def is_closed(cls):         # -> bool
        """ Return whether the Acceptor is closed. """
        pass

    @abstractmethod
    def get_endpoint(cls):      # -> EndPoint
        """ Return the EndPoint associated with the Acceptor. """
        pass
