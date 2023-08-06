import json
from enum import Enum
from box import Box

from turbindo.database.impl.sqlite import SQL_TYPE_LOOKUP
from turbindo.std.streams.stream import Stream
from turbindo.util import get_ondisk_type_map


class SPECIAL_TYPES(Enum):
    NOT_SET = 1


class DataType:
    types = {}

    @staticmethod
    def lookup_datatype(name):
        return DataType.types[name]

    @staticmethod
    def register_datatype(name, type, sqltype):
        DataType.types[name] = type
        SQL_TYPE_LOOKUP[name] = sqltype


class Serialization(Enum):
    STRING = 1
    JSON = 2
    DICT = 3
    PICKLE = 4
    BOX = 5


class TableMetaData:
    def __init__(self, primary_key="id", default_values={}, foreign_keys={}, custom_seralizers={}, unique_fields=[]):
        self._primary_key = primary_key
        self._default_values = default_values
        self._foreign_keys = foreign_keys
        self._custom_seralizers = custom_seralizers
        self._unique_fields = unique_fields

    @property
    def primary_key(self) -> str:
        return self._primary_key

    @property
    def default_values(self) -> dict:
        return self._default_values

    @property
    def foreign_keys(self) -> dict:
        return self._foreign_keys

    @property
    def custom_seralizers(self) -> dict:
        return self._custom_seralizers

    @property
    def unique_fields(self) -> list:
        return self._unique_fields


class AbstractDataTable:
    metadata = TableMetaData()

    DATABASE_IMPL = None

    def __init__(self, id):
        self.objid = id
        self.data: Box = None

    def serialize(self, s: Serialization):
        if s is Serialization.STRING:
            data = {}
            tm = get_ondisk_type_map(self.__class__)
            for k, _ in tm.items():
                data[k] = getattr(self, k)
            return json.dumps(data)
        elif s is Serialization.JSON:
            data = {}
            tm = get_ondisk_type_map(self.__class__)
            for k, _ in tm.items():
                data[k] = getattr(self, k)
            return json.dumps(data)
        elif s is Serialization.DICT:
            data = {}
            tm = get_ondisk_type_map(self.__class__)
            for k, _ in tm.items():
                data[k] = getattr(self, k)
            return data
        elif s is Serialization.BOX:
            data = {}
            tm = get_ondisk_type_map(self.__class__)
            for k, _ in tm.items():
                data[k] = getattr(self, k)
            return Box(data)
        elif s is Serialization.PICKLE:
            raise Exception("PICKLE unimplemented")
        else:
            raise Exception(f"unknown serialization {s}")

    @property
    def id(self) -> str:
        return self.data.id

    async def read(self):
        return await AbstractDataTable.DATABASE_IMPL._read(self, self.objid)

    async def set(self, **kwargs):
        return await AbstractDataTable.DATABASE_IMPL._set(self, self.objid, **kwargs)

    async def delete(self):
        return await AbstractDataTable.DATABASE_IMPL._delete(self, self.objid)

    @classmethod
    async def iterate(cls):
        return await AbstractDataTable.DATABASE_IMPL._iterate(cls)

    @classmethod
    async def stream(cls) -> Stream:
        return await AbstractDataTable.DATABASE_IMPL._stream(cls)

    @classmethod
    async def dumpAll(cls) -> list:
        return await AbstractDataTable.DATABASE_IMPL._dump(cls)

    @classmethod
    async def dumpAllKeys(cls) -> list:
        return await AbstractDataTable.DATABASE_IMPL._dumpKeys(cls)

    @classmethod
    async def truncate(cls) -> list:
        return await AbstractDataTable.DATABASE_IMPL._truncate(cls)

    @classmethod
    async def selectWhere(cls, **kwargs):
        return await AbstractDataTable.DATABASE_IMPL._selectWhere(cls, **kwargs)


class BaseMachineData(AbstractDataTable):
    @property
    def state(self) -> str:
        return self.data.state
