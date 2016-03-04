from . import CacheableAdapter


class DictAdapter(CacheableAdapter):
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
    def list(cls, prefix=None, limit=None):
        res = { k : v for k, v in cls.data.items() if not prefix or k.startswith(prefix) }

        if limit:
            res = res[:limit]

        return res
