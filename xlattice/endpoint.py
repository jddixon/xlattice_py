# xlattice_py/xlattice/endpoint.py

"""
An EndPoint is specified by a Transport and an Address, including
the local part.  If the Transport is TCP/IP, for example, the
Address includes the IP address and the port number.
"""

from abc import ABCMeta, abstractmethod


class EndPoint(metaclass=ABCMeta):
    """ An XLattice EndPoint: the near or far end of a Connection. """

    @abstractmethod
    def get_address(self):       # -> Address
        """ Return the address associated with the EndPoint. """
        pass

    @abstractmethod
    def get_transport(self):     # -> Transport
        """ Return the Transport associated with the EndPoint. """
        pass

    @abstractmethod
    def __str__(self):           # -> str
        """ Return the EndPoint in string form. """
        pass
