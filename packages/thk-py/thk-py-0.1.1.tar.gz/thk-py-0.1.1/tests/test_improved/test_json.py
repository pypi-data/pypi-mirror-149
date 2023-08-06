# -*- coding: utf-8 -*-
import unittest

from thk_py.improved import json


class T(unittest.TestCase):

    def test__fast_json_dumps__success(self):
        self.assertEqual(
            json.fast_dumps({'a': 'b'}),
            '{"a":"b"}'
        )

    def test__fast_json_loads__success(self):
        self.assertEqual(
            json.fast_loads('[1, 2, 3]'),
            [1, 2, 3]
        )
