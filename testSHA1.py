#!/usr/bin/python3

# xlattice_py/testSHA1.py

import binascii, hashlib, os, re, time, unittest
from xlattice   import u
from rnglib     import SimpleRNG

DATA_PATH   = 'myData'      # contains files of random data
U_PATH      = 'myU1'        # those same files stored by content hash
U_TMP_PATH  = 'myU1/tmp'

class TestSHA1 (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG( time.time() )
        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)
        if not os.path.exists(U_PATH):
            os.mkdir(U_PATH)
        if not os.path.exists(U_TMP_PATH):
            os.mkdir(U_TMP_PATH)

    def tearDown(self):
        # probably should clear DATA_PATH and U_PATH directories
        pass

    # utility functions #############################################


    # actual unit tests #############################################
    def testCopyAndPut1(self):
        """we are testing sha1Key = u.copyAndPut1(path, uPath, key) """

        # create a random file                          maxLen   minLen
        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16*1024,    1)
        dKey          = u.fileSHA1Hex(dPath)

        # invoke function
        (uLen, uKey) = u.copyAndPut1(dPath, U_PATH, dKey)
        self.assertEqual(dLen, uLen)
        self.assertEqual(dKey, uKey)

        # verify that original and copy both exist
        self.assertTrue( os.path.exists(dPath) )
        uPath = u.getPathForKey( U_PATH, uKey  )
        self.assertTrue( os.path.exists(uPath) )
    
        dKeyBin = u.fileSHA1Bin(dPath)
        dKeyHex = binascii.b2a_hex(dKeyBin).decode('utf-8')
        self.assertEqual(dKeyHex, dKey)

    def testExists(self):
        """we are testing whether = u.exists(uPath, key) """

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16*1024,    1)
        dKey          = u.fileSHA1Hex(dPath)
        (uLen, uKey) = u.copyAndPut1(dPath, U_PATH, dKey)
        uPath = u.getPathForKey( U_PATH, uKey  )
        self.assertTrue( os.path.exists(uPath) )
        self.assertTrue( u.exists(U_PATH, uKey) )
        os.unlink(uPath)
        self.assertFalse( os.path.exists(uPath) )
        self.assertFalse( u.exists(U_PATH, uKey) )

    def testFileLen(self):
        """we are testing len = u.fileLen(uPath, key) """

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16*1024,    1)
        dKey          = u.fileSHA1Hex(dPath)
        (uLen, uKey) = u.copyAndPut1(dPath, U_PATH, dKey)
        uPath = u.getPathForKey( U_PATH, uKey  )
        self.assertEqual(dLen, uLen)
        self.assertEqual(dLen, u.fileLen(U_PATH, uKey))

    def testFileSHA1(self):
        """ we are testing sha1Key = fileSHA1Hex(path) """
        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16*1024,    1)
        with open(dPath, 'rb') as f:
            data = f.read()
        digest = hashlib.sha1()
        digest.update(data)
        dKey = digest.hexdigest()
        fsha1 = u.fileSHA1Hex(dPath)
        self.assertEqual(dKey, fsha1)

    def testGetPathForKey(self):
        """ we are testing path = getPathForKey(uPath, key) """

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16*1024,    1)
        dKey          = u.fileSHA1Hex(dPath)
        (uLen, uKey) = u.copyAndPut1(dPath, U_PATH, dKey)
        uPath = u.getPathForKey( U_PATH, uKey  )

        # XXX implementation-dependent test
        expectedPath = "%s/%s/%s/%s" % ( U_PATH, uKey[0:2], uKey[2:4], uKey )
        self.assertEqual(expectedPath, uPath)

    def testPut1(self):          
        """we are testing (len,hash)  = put1(inFile, uPath, key) """

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16*1024,    1)
        dKey          = u.fileSHA1Hex(dPath)
        with open(dPath, 'rb') as f:
            data = f.read()
        dupePath = os.path.join(DATA_PATH, dKey)
        with open(dupePath, 'wb') as f:
            f.write(data)

        (uLen, uKey) = u.put1(dPath, U_PATH, dKey)
        uPath = u.getPathForKey( U_PATH, uKey  )

        # inFile is renamed
        self.assertFalse( os.path.exists(dPath)  )
        self.assertTrue ( u.exists(U_PATH, uKey) )

        (dupeLen, dupeKey) = u.put1(dupePath, U_PATH, dKey)
        # dupe file is deleted'
        self.assertEqual( uKey, dupeKey )
        self.assertFalse( os.path.exists(dupePath)  )
        self.assertTrue ( u.exists(U_PATH, uKey) )

    def testPutData1(self):    
        """ we are testing (len,hash)  = putData1(data, uPath, key) """
        
        # this is just lazy coding ;-)
        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16*1024,    1)
        dKey          = u.fileSHA1Hex(dPath)
        with open(dPath, 'rb') as f:
            data = f.read()

        (uLen, uKey) = u.putData1(data, U_PATH, dKey)
        self.assertEqual(dKey, uKey)
        self.assertTrue (u.exists(U_PATH, dKey))
        uPath = u.getPathForKey( U_PATH, uKey  )


if __name__ == '__main__':
    unittest.main()
