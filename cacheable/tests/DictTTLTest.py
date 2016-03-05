#!/usr/bin/python

import os
import sys
from time import sleep
from time import time
import unittest

sys.path = [ os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) ] + sys.path

from cacheable import Cacheable
from cacheable.adapter import DictAdapter
from cacheable.adapter import PeeweeAdapter
from peewee import SqliteDatabase


class TimeCacheable(Cacheable):
    @staticmethod
    def load_data(keys):
        return { x : int(time()) for x in keys }


class TimeTTLCacheable(Cacheable):
    TTL = 1

    @staticmethod
    def load_data(keys):
        return { x : int(time()) for x in keys }


class DictTTLTest(unittest.TestCase):
    def setUp(self):
        self.adapter = DictAdapter()
        Cacheable.init(self.adapter)

    def test_basic(self):
        ts = time()
        res = TimeCacheable.get('abc')
        self.assertTrue(abs(res - ts) <= 1)

        res2 = TimeCacheable.get('abc')
        self.assertEqual(res, res2)

        sleep(1.5)
        res3 = TimeCacheable.get('abc')
        self.assertEqual(res, res3)


    def test_expired(self):
        res = TimeTTLCacheable.get('abc')

        sleep(2)
        res2 = TimeTTLCacheable.get('abc')
        self.assertNotEqual(res, res2)


if __name__ == '__main__':
    unittest.main()
