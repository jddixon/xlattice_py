# xlattice_py/xlattice/connector.py

"""
An XLattice Connector, used to establish a Connection with another entity
(Node).

The notion is that a node has a collection of Connectors used
for establishing Connections with Peers, neighboring nodes.
"""

from abc import ABCMeta, abstractmethod


class Connector(metaclass=ABCMeta):
    """ Used to establish a Connetion with another Node-like entity. """

    @abstractmethod
    def connect(self, near_end, blocking):            # raises IOException
        """
        Establish a Connection with another entity using the transport
        and address in the EndPoint.

        @param nearEnd  local end point to use for connection
        @param blocking whether the new Connection is to be blocking
        @raises IOException if not in appropriate state
        """
        pass

    def get_far_end(self):       # -> EndPoint
        """
        Return the Acceptor EndPoint that this Connector is used to
        establish connections to
        """
        pass
