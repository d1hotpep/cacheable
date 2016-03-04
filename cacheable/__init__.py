__author__ = 'dpepper'
__version__ = '0.1.0'


from inspect import isclass
import types

from adapter import CacheableAdapter


class Cacheable:
    ADAPTER = None
    VERSION = 1


    def __init__(self):
        raise Exception('usage error, call init()')

    @classmethod
    def init(cls, adapter):
        assert isclass(adapter), 'expected a class, found %s' % type(adapter)
        assert issubclass(adapter, CacheableAdapter),  \
            'expected a %s, found %s' % (CacheableAdapter.__name__, adapter)

        cls.ADAPTER = adapter


    @classmethod
    def cachekey_prefix(cls):
        return '%s:%s:' % (cls.__name__.lower(), cls.VERSION)


    @classmethod
    def cachekeys(cls, keys):
        prefix = cls.cachekey_prefix()
        cachekeys = {}

        for key in keys:
            cachekeys[key] = '%s%s' % (prefix, key)

        return cachekeys

    @classmethod
    def cachekey(cls, key):
        return cls.cachekeys([ key ]).get(key)


    @classmethod
    def multiget(cls, keys):
        cachekeys = cls.cachekeys(keys)

        if not hasattr(cls, 'LOCAL_CACHE'):
            # initialize here instead of at class level so that each
            # subclass has it's own cache, instead of the same global one
            cls.LOCAL_CACHE = {}

        # check local cache
        missing_keys = set(keys)
        for key in list(missing_keys):
            if cls.LOCAL_CACHE.has_key(key):
                missing_keys.remove(key)

        # check DB cache
        if missing_keys:
            kv = cls.ADAPTER.multiget([ cachekeys[key] for key in missing_keys ])
            for key in list(missing_keys):
                if kv.has_key(cachekeys[key]):
                    cls.LOCAL_CACHE[key] = kv[cachekeys[key]]
                    missing_keys.remove(key)

        if missing_keys:
            data = cls.load_data(list(missing_keys))
            if set(data.keys()) != set(missing_keys):
                raise Exception('%s::load_data() did not return all values' % cls.__name__)

            cls.ADAPTER.multiset({ cachekeys[key] : value for key, value in data.items() })
            cls.LOCAL_CACHE.update(data)

        return { key : cls.LOCAL_CACHE[key] for key in keys }

    @classmethod
    def get(cls, key):
        return cls.multiget([ key ]).get(key)


    @classmethod
    def delete(cls, key_or_keys):
        if list == type(key_or_keys):
            keys = key_or_keys
        else:
            keys = [ key_or_keys ]

        cachekeys = cls.cachekeys(keys)

        cls.ADAPTER.delete(cachekeys.values())
        for key in cachekeys:
            if hasattr(cls, 'LOCAL_CACHE') and cls.LOCAL_CACHE.has_key(key):
                del cls.LOCAL_CACHE[key]


    @classmethod
    def list(cls, limit=None):
        prefix = cls.cachekey_prefix()
        return cls.ADAPTER.list(prefix, limit)


    @staticmethod
    def load_data(keys):
        raise NotImplementedError
