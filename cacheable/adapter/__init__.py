"""
Plumming to connect the Cacheable layer to some storage
"""

class CacheableAdapter:
    @staticmethod
    def multiget(keys):
        raise NotImplementedError

    @classmethod
    def get(cls, key):
        return cls.multiget([ key ]).get(key)

    @staticmethod
    def multiset(data):
        raise NotImplementedError

    @classmethod
    def set(cls, key, value):
        cls.multiset({ key : value })

    @staticmethod
    def delete(keys):
        raise NotImplementedError

    @staticmethod
    def list(prefix=None, limit=None):
        raise NotImplementedError


from DictAdapter import DictAdapter

try:
    import peewee
    from PeeweeAdapter import PeeweeAdapter
except ImportError:
    pass
