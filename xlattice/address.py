# xlattice_py/xlattice/Address.py

"""
The XLattice Address abstraction.

An Address provides enough information to identify an EndPoint.
The information needed depends upon the communications protocol
used.  An EndPoint has one and only one Address.

"""

from abc import ABCMeta, abstractmethod


class Address(ABCMeta):
    """ XLattice's Address abstraction. """

    @abstractmethod
    def __eq__(cls, other):         # -> bool
        """ Whether this Address equals another. """
        return False

    @abstractmethod
    def hashcode(cls):              # -> int
        """ Return a reasonably distributed hash for the Address. """
        return 0

    @abstractmethod
    def __str__(cls):               # -> str
        """ Return a string representation of the Address. """
        pass
