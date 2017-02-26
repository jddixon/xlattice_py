# xlattice_py/xlattice/protocol.py

""" Abstracts a family of messages. """

from abc import ABCMeta, abstractmethod


class Protocol(metaclass=ABCMeta):
    """ Abstracts a family of messages. """

    @property
    @abstractmethod
    def name(self):
        """
        Return the name of the protocol, which must be unique
        within the context.
        """
