#!/usr/bin/python

import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from cacheable import Cacheable
from DictAdapter import Adapter


class LengthCacheable(Cacheable):
    @staticmethod
    def load_data(keys):
        return { x : len(x) for x in keys }


class LengthV2Cacheable(LengthCacheable):
    VERSION = 2

    @staticmethod
    def load_data(keys):
        return { x : 2 * len(x) for x in keys }


class CacheableTest(unittest.TestCase):
    def setUp(self):
        Cacheable.init(Adapter())


    def basic_test(self):
        self.assertEmpty(LengthCacheable.list(prefix=''))

        res = LengthCacheable.get('abc')
        self.assertEquals(res, 3)

        self.assertEquals(LengthCacheable.list(prefix=''), { 'abc' : 3 })

        res = LengthCacheable.get('z')
        self.assertEquals(res, 1)

        res = LengthCacheable.multiget(['abc', 'z'])
        self.assertEquals(res, { 'abc' : 3, 'z' : 1 })


    def versions_test(self):
        self.assertEmpty(LengthCacheable.list(prefix=''))
        self.assertEmpty(LengthV2Cacheable.list(prefix=''))

        res = LengthCacheable.get('abc')
        self.assertEquals(res, 3)
        self.assertNotEmpty(LengthCacheable.list(prefix=''))
        self.assertEmpty(LengthV2Cacheable.list(prefix=''))

        res = LengthV2Cacheable.get('abc')
        self.assertEquals(res, 6)
        res = LengthCacheable.get('abc')
        self.assertEquals(res, 3)



if __name__ == '__main__':
    unittest.main()
