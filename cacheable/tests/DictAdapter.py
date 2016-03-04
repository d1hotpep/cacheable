import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from cacheable import Cacheable
from cacheable import CacheableAdapter


class Adapter(CacheableAdapter):
    data = {}

    @classmethod
    def multiget(cls, keys):
        return { k : v for k, v in cls.data.items() if k in keys }

    @classmethod
    def multiset(cls, data):
        cls.data.update(data)

    @classmethod
    def delete(cls, keys):
        for key in keys:
            del cls.data[key]

    @classmethod
    def list(cls, prefix, limit=None):
        res = { k : v for k, v in cls.data.items() if k.startswith(prefix) }

        if limit:
            res = res[:limit]

        return res
