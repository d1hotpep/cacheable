#!/usr/bin/python

import os
import sys
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) ] + sys.path

from cacheable import Cacheable
from cacheable.adapter import DictAdapter


class LengthCacheable(Cacheable):
    @staticmethod
    def load_data(keys):
        return { x : len(x) for x in keys }


class LengthV2Cacheable(Cacheable):
    VERSION = 2

    @staticmethod
    def load_data(keys):
        return { x : 2 * len(x) for x in keys }


class CacheableTest(unittest.TestCase):
    def setUp(self):
        self.adapter = DictAdapter()
        Cacheable.init(self.adapter)


    def test_basic(self):
        self.assertFalse(LengthCacheable.list())

        res = LengthCacheable.get('abc')
        self.assertEquals(res, 3)

        self.assertEquals(len(LengthCacheable.list()), 1)

        res = LengthCacheable.get('z')
        self.assertEquals(res, 1)

        res = LengthCacheable.multiget(['abc', 'z'])
        self.assertEquals(res, { 'abc' : 3, 'z' : 1 })


    def test_version(self):
        # local cache persisted
        self.assertTrue(LengthCacheable.list())

        # but this one is new too
        self.assertFalse(LengthV2Cacheable.list())

        res = LengthCacheable.get('abc')
        self.assertEquals(res, 3)
        self.assertTrue(LengthCacheable.list())
        self.assertFalse(LengthV2Cacheable.list())

        res = LengthV2Cacheable.get('a')
        self.assertEquals(res, 2)

        res = LengthV2Cacheable.get('abc')
        self.assertEquals(res, 6)
        res = LengthCacheable.get('abc')
        self.assertEquals(res, 3)



if __name__ == '__main__':
    unittest.main()
