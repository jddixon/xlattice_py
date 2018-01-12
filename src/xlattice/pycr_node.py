# ~/dev/py/xlattice_py/xlattice/pycr_node.py

"""
XLattice Node functionality using pycrypto for RSA functions.

This code will only be used temporarily, while AbstractNode is being
sorted out.
"""

import os
import sys
import hashlib
import warnings

from Crypto.PublicKey import RSA as rsa

from xlattice import HashTypes, check_hashtype  # , UnrecognizedSHAError

if sys.version_info < (3, 6):
    # pylint: disable=unused-import
    import sha3
    assert sha3     # suppress warning


class PyCrNode(object):
    """
    Parent class for Node-like things using pycrypto RSA.

    The class formerly known as AbstractNode.
    """

    def __init__(self, hashtype=HashTypes.SHA2, pub_key=None, node_id=None):

        warnings.warn("deprecated: use xlnode_py instead")

        check_hashtype(hashtype)
        self._hashtype = hashtype
        if node_id is None:
            if pub_key:
                # DEBUG
                print("PyCrNode: public key is %s" % str(pub_key))
                print("              class is %s" % pub_key.__class__)
                # END

                # we have called checkUsingSHA(): one of these cases must apply
                if hashtype == HashTypes.SHA1:
                    sha = hashlib.sha1()
                elif hashtype == HashTypes.SHA2:
                    sha = hashlib.sha256()
                elif hashtype == HashTypes.SHA3:
                    sha = hashlib.sha3_256
                sha.update(pub_key.exportKey())
                node_id = sha.digest()    # a binary value
            else:
                raise ValueError('cannot calculate nodeID without pubKey')

        self._node_id = node_id
        self._pub_key = pub_key

    @property
    def node_id(self):
        """ Return the 160- or 256-bit node ID. """
        return self._node_id

    @property
    def pub_key(self):
        """ Return the public part of the Node's RSA key. """
        return self._pub_key


class Node(PyCrNode):
    """
    The cryptographic identity of an pycrypto-based XLattice Node: its
    nodeID and RSA keys.
    """

    def __init__(self, hashtype=HashTypes.SHA2, priv_key=None):

        # making this the default value doesn't work: it always
        # generates the same key
        if priv_key is None:
            priv_key = rsa.generate(2048, os.urandom)
        node_id, pub_key = Node.calc_id_and_pub_key_for_node(
            hashtype, priv_key)
        PyCrNode.__init__(self, hashtype, pub_key, node_id)

        if not priv_key:
            raise ValueError('INTERNAL ERROR: undefined private key')
        self._private_key = priv_key

        # each of these needs some sort of map or maps, or we will have to do
        # a linear search
        self._peers = []
        self._overlays = []    #
        self._connections = []    # with peers? with clients?

    def create_from_key(self, string):
        """
        Given the serialization of a node, create one.


        Despite the name, this should also handle peer lists, etc.

        XXX WE ALSO NEED a serialization function
        """
        pass

    @staticmethod
    def calc_id_and_pub_key_for_node(hashtype, rsa_priv_key):
        """ Calculate a NodeID and public key, given an RSA private key. """
        check_hashtype(hashtype)
        (node_id, pub_key) = (None, None)
        pub_key = rsa_priv_key.publickey()

#       # DEBUG
#       print "GET_ID: private key is %s" % str(rsaPrivateKey.__class__)
#       print "    has_private = %s" % rsaPrivateKey.has_private()
#       print "GET_ID: public key is  %s" % str(pubKey.__class__)
#       print "    has_private = %s" % pubKey.has_private()
#       # END

        # generate the nodeID from the public key
        if hashtype == HashTypes.SHA1:
            sha = hashlib.sha1()
        elif hashtype == HashTypes.SHA2:
            sha = hashlib.sha256()
        elif hashtype == HashTypes.SHA3:
            sha = hashlib.sha3_256()

        sha.update(pub_key.exportKey())
        node_id = sha.digest()
        return (node_id,                 # nodeID = 160/256 bit BINARY value
                pub_key)                 # from private key

    @property
    def key(self):
        """ Return this node's RSA private key. """
        return self._private_key

    # these work with
    def sign(self, msg):
        """ Sign a message using this node's private key. """
        sha = hashlib.sha1()
        sha.update(bytes(msg))
        d_val = sha.digest()
        return self._private_key.sign(d_val, msg)

    def verify(self, msg, signature):
        """ Verify the digital signature using this node's private key. """
        sha = hashlib.sha1()
        sha.update(bytes(msg))
        d_val = sha.digest()
        return self._pub_key.verify(d_val, signature)


class Peer(PyCrNode):
    """ a Peer is a Node seen from the outside """

    def __init__(self, hashtype=HashTypes.SHA2, node_id=None, pub_key=None):
        PyCrNode.__init__(self, hashtype, node_id, pub_key)
