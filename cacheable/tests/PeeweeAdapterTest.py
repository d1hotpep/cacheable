#!/usr/bin/python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) ] + sys.path

from cacheable import Cacheable
from cacheable.adapter import PeeweeAdapter
from peewee import SqliteDatabase


class LengthCacheable(Cacheable):
    @staticmethod
    def load_data(keys):
        return { x : len(x) for x in keys }


class PeeweeAdapterTest(unittest.TestCase):
    def setUp(self):
        database = SqliteDatabase(':memory:')
        self.adapter = PeeweeAdapter(database)
        PeeweeAdapter.create_table()

        Cacheable.init(self.adapter)


    def test_basic(self):
        self.assertFalse(LengthCacheable.list())

        res = LengthCacheable.get('abc')
        self.assertEquals(res, 3)

        self.assertEquals(len(LengthCacheable.list()), 1)

        LengthCacheable.delete('abc')
        self.assertEquals(len(LengthCacheable.list()), 0)

        res = LengthCacheable.get('z')
        self.assertEquals(res, 1)

        res = LengthCacheable.multiget(['abc', 'z'])
        self.assertEquals(res, { 'abc' : 3, 'z' : 1 })

        self.assertEquals(len(LengthCacheable.list()), 2)


if __name__ == '__main__':
    unittest.main()
