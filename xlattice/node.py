# ~/dev/py/xlattice_py/xlattice/node.py

import os
import sys
import hashlib
import sha3

from Crypto.PublicKey import RSA as rsa
#from Crypto.Signature       import PKCS1_PSS    as pkcs1
from Crypto.Signature import PKCS1_v1_5 as pkcs1

from xlattice import Q, check_using_sha, UnrecognizedSHAError


class AbstractNode(object):

    def __init__(self, using_sha=False, pub_key=None, node_id=None):

        check_using_sha(using_sha)
        self._usingSHA = using_sha
        if node_id is None:
            if pub_key:
                # DEBUG
                print("AbstractNode: public key is %s" % str(pub_key))
                print("              class is %s" % pub_key.__class__)
                # END

                # we have called checkUsingSHA(): one of these cases must apply
                if using_sha == Q.USING_SHA1:
                    h = hashlib.sha1()
                elif using_sha == Q.USING_SHA2:
                    h = hashlib.sha256()
                elif using_sha == Q.USING_SHA3:
                    h = hashlib.sha3_256
                h.update(pub_key.exportKey())
                node_id = h.digest()    # a binary value
            else:
                raise ValueError('cannot calculate nodeID without pubKey')

        self._nodeID = node_id
        self._pubKey = pub_key

    @property
    def node_id(self): return self._nodeID

    @property
    def pub_key(self): return self._pubKey


class Node(AbstractNode):
    """
    """

    def __init__(self, using_sha=Q.USING_SHA2, priv_key=None):

        # making this the default value doesn't work: it always
        # generates the same key
        if priv_key is None:
            priv_key = rsa.generate(2048, os.urandom)
        node_id, pub_key = Node.get_id_and_pub_key_for_node(
            using_sha, self, priv_key)
        AbstractNode.__init__(self, using_sha, pub_key, node_id)

        if not priv_key:
            raise ValueError('INTERNAL ERROR: undefined private key')
        self._privateKey = priv_key

        # each of these needs some sort of map or maps, or we will have to do
        # a linear search
        self._peers = []
        self._overlays = []    #
        self._connections = []    # with peers? with clients?

    def createFromKey(self, string):
        # XXX STUB: given the serialization of a node, create one
        # despite the name, this should also handle peer lists, etc
        # XXX WE ALSO NEED a serialization function
        pass

    @staticmethod
    def get_id_and_pub_key_for_node(using_sha, node, rsa_priv_key):

        check_using_sha(using_sha)
        (node_id, pub_key) = (None, None)
        pub_key = rsa_priv_key.publickey()

#       # DEBUG
#       print "GET_ID: private key is %s" % str(rsaPrivateKey.__class__)
#       print "    has_private = %s" % rsaPrivateKey.has_private()
#       print "GET_ID: public key is  %s" % str(pubKey.__class__)
#       print "    has_private = %s" % pubKey.has_private()
#       # END

        # generate the nodeID from the public key
        if using_sha == Q.USING_SHA1:
            h = hashlib.sha1()
        elif using_sha == Q.USING_SHA2:
            h = hashlib.sha256()
        elif using_sha == Q.USING_SHA3:
            h = hashlib.sha3_256()

        h.update(pub_key.exportKey())
        node_id = h.digest()
        return (node_id,                 # nodeID = 160/256 bit BINARY value
                pub_key)                 # from private key

    @property
    def key(self):
        return self._privateKey

    # these work with
    def sign(self, msg):
        h = hashlib.sha1()
        h.update(bytes(msg))
        dVal = h.digest()
        return self._privateKey.sign(dVal, msg)

    def verify(self, msg, signature):
        h = hashlib.sha1()
        h.update(bytes(msg))
        dVal = h.digest()
        return self._pubKey.verify(dVal, signature)


class Peer(AbstractNode):
    """ a Peer is a Node seen from the outside """

    def __init__(self, using_sha=False, node_id=None, pub_key=None):
        AbstractNode.__init__(self, using_sha, node_id, pub_key)
