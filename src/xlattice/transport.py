# xlattice_py/xlattice/transport.py

"""
Abstraction of the transport protocol used over a communications
channel.

XXX As it has been interpreted so far, this is unsatisfactory.
For example, if there are several nodes on a host, each will have its
own keystore.  If the Transport is Tls, any Acceptor created through
this interface would need to have access to that keystore.  Therefore
what's needed is an instance of a Transport provider/factory associated
with the node, with a reference to the keystore either in the
  def Acceptor getAcceptor   (Address near, boolean blocking)
                                              raises IOException
constructor or passed in a setter.

Dichotomies are: blocking versus non-blocking, reliable vs unreliable.
"""

from abc import ABCMeta, abstractmethod


class Transport(metaclass=ABCMeta):
    """
    The XLattice Transport absraction.

    XLattice Java v0.3.8 distinguishes connection-oriented transports
    (tls, tcp) from connectionless (udp)
    """

    @abstractmethod
    def get_acceptor(self):          # -> Acceptor
        """
        Create an Acceptor with the local address specified.  The
        Acceptor listens for attempts to establish connections on
        that address and then creates connections to the contacting
        node (client) possibly on the same local address, possibly
        on another, according to the transport protocol.

        XXX Need to be able to specify the protocol for the
        XXX connection created and whether that connection is blocking
        XXX need an AcceptorListener (default should be same protocol,
        XXX and non-blocking).

        @param near     local address on which the Acceptor listens
        @param blocking whether the Acceptor itself blocks
        """
        pass

    @abstractmethod
    def get_connection(self, near, far, blocking):
        """
        Return a Connection between Addresses near and far; this may or may
        not blocking.

        # Java note: THIS SHOULD BE DROPPED ENTIRELY
        """
        pass

    @abstractmethod
    def get_connector(self, far, blocking):   # -> Connector, raises IOError
        """
        Get a Connector for use in setting up connections to a
        remote host.  The Connector itself may be blocking or non-blocking
        that is, Connector.connect() may or may not block.  That is
        specified here.  Whether the new Connection is itself blocking
        is determined by a Connector.connect() parameter.

        @param far      address of the remote Acceptor
        @param blocking whether this Connector is itself blocking
        """
        pass

    @abstractmethod
    def name(self):     # -> str
        """ Return a name for this transport protocol, useful in debugging. """
        pass
