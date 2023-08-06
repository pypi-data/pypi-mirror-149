import json

from aiosqlite import Connection

SQL_NATIVE_TYPE_LIST = ["bool", "str", "int"]
SQL_TYPE_LOOKUP = {
    'bool': "BOOLEAN",
    'str': "TEXT",
    'int': "INTEGER",
    'datetime': "INTEGER",
    # @encoding json
    'list': "TEXT",
    # @encoding json
    'dict': "TEXT"
}
SQL_TYPE_SERIALIZERS = {
    "datetime": lambda dt: dt.timestamp(),
    "list": lambda lst: json.dumps(lst),
    "dict": lambda dct: json.dumps(dct),
    "EntryType": lambda et: int(et)
}


def sqlite_type_rev_lookup(sqltype: str) -> str:
    for k, v in SQL_TYPE_LOOKUP.items():
        if v == sqltype:
            return k
    raise Exception(f"sql type {sqltype} not found")


class Sqlite:
    conn: Connection = None

    @classmethod
    async def query(cls, query_string):
        cursor = await Sqlite.conn.execute(query_string)
        await Sqlite.conn.commit()
        return cursor
