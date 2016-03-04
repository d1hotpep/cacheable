import peewee
import playhouse.kv

from . import CacheableAdapter


database_proxy = peewee.Proxy()


class PeeweeAdapter(CacheableAdapter, peewee.Model):
    key = peewee.CharField(max_length=256, unique=True)
    value = playhouse.kv.JSONField()

    class Meta:
        database = database_proxy


    @classmethod
    def init(cls, db_connection, table_name=None):
        global database_proxy

        if table_name:
            cls._meta.db_table = table_name

        database_proxy.initialize(db_connection)


    @classmethod
    def multiget(cls, keys):
        res = cls.select(cls.key, cls.value).where(cls.key << keys).tuples()
        return {
            x[0] : x[1] for x in res
        }

    @classmethod
    def multiset(cls, data):
        kvs = [ { cls.key : key, cls.value : value } for key, value in data.items() ]
        cls.insert_many(kvs).upsert().execute()


    @classmethod
    def delete(cls, key_or_keys):
        if list == type(key_or_keys):
            keys = key_or_keys
        else:
            keys = [ key_or_keys ]

        super(cls, cls).delete().where(cls.key << keys).execute()


    @classmethod
    def list(cls, prefix=None, limit=None):
        q = cls.select(cls.key, cls.value)

        if prefix:
            if type(cls._meta.database.obj) == peewee.SqliteDatabase:
                wildcard = '*'
            else:
                wildcard = '%'

            q = q.where(cls.key % ('%s%s' % (prefix, wildcard)))

        if limit:
            q = q.limit(limit)

        res = { x[0] : x[1] for x in q.tuples() }

        if prefix:
            res = { k[len(prefix):] : v for k, v in res.items() }

        return res
