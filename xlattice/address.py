# xlattice_py/xlattice/Address.py

"""
The XLattice Address abstraction.

An Address provides enough information to identify an EndPoint.
The information needed depends upon the communications protocol
used.  An EndPoint has one and only one Address.

"""

from abc import ABCMeta, abstractmethod


class Address(metaclass=ABCMeta):
    """ XLattice's Address abstraction. """

    @abstractmethod
    def __eq__(self, other):         # -> bool
        """ Whether this Address equals another. """
        return False

    @abstractmethod
    def hashcode(self):              # -> int
        """ Return a reasonably distributed hash for the Address. """
        return 0

    @abstractmethod
    def __str__(self):               # -> str
        """ Return a string representation of the Address. """
        pass
