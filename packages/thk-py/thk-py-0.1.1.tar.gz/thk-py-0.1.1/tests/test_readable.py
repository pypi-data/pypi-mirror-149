# -*- coding: utf-8 -*-
import unittest

from thk_py import readable


class T(unittest.TestCase):

    def test__get_readable_size__success(self):
        self.assertEqual(
            readable.get_readable_size(10000),
            '9.77KB'
        )
