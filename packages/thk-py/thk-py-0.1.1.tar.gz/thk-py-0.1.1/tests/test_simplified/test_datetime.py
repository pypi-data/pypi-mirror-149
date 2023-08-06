# -*- coding: utf-8 -*-
import unittest
from datetime import datetime, date, timedelta

from thk_py.simplified import datetime as dt


class T(unittest.TestCase):

    def test__str2date__success(self):
        self.assertEqual(
            dt.str2date('2020-03-01'),
            date(2020, 3, 1)
        )

    def test__str2datetime__success(self):
        self.assertEqual(
            dt.str2datetime('2020-03-01 10:01:13'),
            datetime(2020, 3, 1, 10, 1, 13)
        )

    def test__date2str__success(self):
        self.assertEqual(
            dt.date2str(date(2019, 10, 3)),
            '2019-10-03'
        )

    def test__datetime2str__success(self):
        self.assertEqual(
            dt.datetime2str(datetime(2010, 12, 1, 10, 11, 13)),
            '2010-12-01 10:11:13'
        )

    def test__timestamp2datetime__success(self):
        self.assertEqual(
            dt.timestamp2datetime(1593706888),
            datetime(2020, 7, 3, 0, 21, 28)
        )

    def test__datetime2timestamp__success(self):
        self.assertEqual(
            dt.datetime2timestamp(datetime(2020, 7, 3, 0, 21, 28)),
            1593706888
        )

    def test__date_range(self):
        first_date = date(2020, 1, 1)
        last_date = date(2020, 1, 5)
        i = 0
        for day in dt.date_range(first_date, last_date):
            self.assertEqual(day, first_date + timedelta(days=i))
            i += 1

    def test__date_range_reversed(self):
        first_date = date(2020, 1, 1)
        last_date = date(2020, 1, 5)
        i = 0
        for day in dt.date_range_reversed(first_date=first_date, last_date=last_date):
            self.assertEqual(day, last_date - timedelta(days=i))
            i += 1

    def test__build_first_datetime(self):
        self.assertEqual(
            dt.datetime2str(dt.build_first_datetime(day=date(2020, 1, 1))),
            '2020-01-01 00:00:00'
        )

        self.assertTrue(
            dt.datetime2str(dt.build_first_datetime()).endswith("00:00:00")
        )

    def test__build_last_datetime(self):
        self.assertEqual(
            dt.datetime2str(dt.build_last_datetime(day=date(2020, 1, 1))),
            '2020-01-01 23:59:59'
        )
        self.assertTrue(
            dt.datetime2str(dt.build_last_datetime()).endswith("23:59:59")
        )


