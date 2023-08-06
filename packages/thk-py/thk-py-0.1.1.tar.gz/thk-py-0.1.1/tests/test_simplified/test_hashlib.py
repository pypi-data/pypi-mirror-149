# -*- coding: utf-8 -*-
import unittest

from thk_py.simplified import hashlib


class T(unittest.TestCase):

    def test__hash_md5__success(self):
        self.assertEqual(
            hashlib.hash_md5('123456'),
            'e10adc3949ba59abbe56e057f20f883e'
        )

    def test__hash_sha1__success(self):
        self.assertEqual(
            hashlib.hash_sha1('123456'),
            '7c4a8d09ca3762af61e59520943dc26494f8941b'
        )

    def test__hash_sha256__success(self):
        self.assertEqual(
            hashlib.hash_sha256('123456'),
            '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
        )

    def test__hash_sha384__success(self):
        self.assertEqual(
            hashlib.hash_sha384('123456'),
            '0a989ebc4a77b56a6e2bb7b19d995d185ce44090c13e2984b7ecc6d446d4b61ea9991b76a4c2f04b1b4d244841449454'
        )

    def test__hash_sha512__success(self):
        self.assertEqual(
            hashlib.hash_sha512('123456'),
            'ba3253876aed6bc22d4a6ff'
            '53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413'
        )
