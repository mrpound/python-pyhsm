# Copyright (c) 2011, Yubico AB
# All rights reserved.

import sys
import unittest
import pyhsm

import test_common

class TestAEAD(test_common.YHSM_TestCase):

    def setUp(self):
        test_common.YHSM_TestCase.setUp(self, debug=True)
        self.nonce = "4d4d4d4d4d4d".decode('hex')
        self.key = "A" * 16
        self.uid = '\x4d\x01\x4d\x02\x4d\x03'
        self.secret = pyhsm.secrets_cmd.YHSM_YubiKeySecret(self.key, self.uid)

    def test_generate_aead_simple(self):
        """ Test generate_aead_simple. """
        # Enabled flags 00000002 = YSM_AEAD_GENERATE
        # HSM> < keyload - Load key data now using flags 00000002. Press ESC to quit
        # 00000002 - stored ok
        key_handle = 2
        aead = self.hsm.generate_aead_simple(self.nonce, key_handle, self.secret)

        self.assertEqual(aead.nonce, self.nonce)
        self.assertEqual(aead.key_handle, key_handle)

        # test that the YubiHSM validates the generated AEAD
        self.assertTrue(self.hsm.validate_aead(self.nonce, key_handle, aead))

    def test_generate_aead_simple2(self):
        """ Test generate_aead_simple wrong key handle. """
        key_handle = 1
        try:
            aead = self.hsm.generate_aead_simple(self.nonce, key_handle, self.secret)
            self.fail("Expected YSM_FUNCTION_DISABLED, got %s" % (res))
        except pyhsm.exception.YHSM_CommandFailed, e:
            self.assertEquals(e.status, pyhsm.defines.YSM_FUNCTION_DISABLED)
