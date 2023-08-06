import inspect

from box import Box
from jinja2 import Environment, BaseLoader

import turbindo
import turbindo.database.impl.sqlite.methods
from turbindo.database.impl.sqlite import SQL_TYPE_SERIALIZERS, SQL_NATIVE_TYPE_LIST
from turbindo.runtime.exceptions import NoRowFoundException
from turbindo.database.base_object import AbstractDataTable
from turbindo.database.default import SPECIAL_TYPES
from turbindo.log.logger import Logger
from turbindo.util import get_ondisk_type_map, get_object_type_map


class SqliteDataTable(AbstractDataTable):
    logger: Logger = Logger("SqliteDataTable")

    @staticmethod
    def is_native_type(type_name) -> bool:
        return type_name in SQL_NATIVE_TYPE_LIST

    @staticmethod
    def get_serializer(type_name) -> callable:
        return SQL_TYPE_SERIALIZERS[type_name]

    @staticmethod
    async def _read(dataobj, primary_key):
        tablename = dataobj.__class__.__name__
        select_statement = f'SELECT * FROM {tablename} WHERE id=?;'
        row, names = await turbindo.database.impl.sqlite.methods.select_from_table(select_statement, primary_key)
        rowDictionary = {}
        if row is not None:
            for i in range(len(names)):
                try:
                    rowDictionary[names[i]] = row[i]
                except IndexError as e:
                    SqliteDataTable.logger.error(e)
            dataobj.data = Box(rowDictionary)
        return dataobj

    @staticmethod
    async def _set(dataobj, primary_key, **kwargs):
        tablename = dataobj.__class__.__name__
        insert_template = """
                    INSERT INTO {{ tablename }}( {% for column in columns %}{{ column }},{% endfor %}id ) 
                    VALUES ({% for column in columns %} ?, {% endfor %}?)
                    """
        update_template = """
                    UPDATE {{ tablename }} SET {% for column in columns %}{{ column }}=?,{% endfor %}id=? WHERE id=?
                    """
        select_template = f'SELECT id FROM {tablename} WHERE id=?;'
        annotation_types = get_object_type_map(dataobj.__class__)

        used_column_values = {}
        for k, v in kwargs.items():
            if not SqliteDataTable.is_native_type(annotation_types[k]):
                serialize = SqliteDataTable.get_serializer(annotation_types[k])
                if v != SPECIAL_TYPES.NOT_SET:
                    v = serialize(v)
            if v is not SPECIAL_TYPES.NOT_SET:
                used_column_values[k] = v

        select_jinja_template = Environment(loader=BaseLoader).from_string(select_template)
        select_statement = select_jinja_template.render()
        exists = True
        try:
            await turbindo.database.impl.sqlite.methods.select_from_table(select_statement, primary_key)
        except NoRowFoundException:
            exists = False

        if not exists:
            jinja_template = Environment(loader=BaseLoader).from_string(insert_template)
            insert_statement = jinja_template.render({
                "tablename": tablename,
                "columns": used_column_values.keys(),
            })
            data_tuple = tuple(used_column_values.values()) + tuple([primary_key])
            await turbindo.database.impl.sqlite.methods.execute_sql_statement(insert_statement, data_tuple)

        else:
            jinja_template = Environment(loader=BaseLoader).from_string(update_template)
            update_statement = jinja_template.render({
                "tablename": tablename,
                "columns": used_column_values.keys(),
            })
            data_tuple = tuple(used_column_values.values()) + tuple([primary_key]) + tuple([primary_key])
            await turbindo.database.impl.sqlite.methods.execute_sql_statement(update_statement, data_tuple)

    @staticmethod
    async def _delete(dataobj, primary_key):
        tablename = dataobj.__class__.__name__
        select_statement = f'DELETE FROM {tablename} WHERE id=?;'
        await turbindo.database.impl.sqlite.methods.execute_sql_statement(select_statement, (primary_key,))

    @staticmethod
    async def _truncate(cls):
        tablename = cls.__name__
        select_statement = f'DELETE FROM {tablename};'
        result = await turbindo.database.impl.sqlite.methods.execute_sql_statement(select_statement, ())

    @staticmethod
    async def _dump(cls):
        table = cls.__name__
        query = f"SELECT * FROM {table}"
        cursor = await turbindo.database.execute_sql_statement(query)
        names = list(map(lambda x: x[0], cursor.description))
        results = []
        for record in await cursor.fetchall():
            data = {}
            for x in range(0, len(names)):
                data[names[x]] = record[x]
            obj = cls(data['id'])
            obj.data = Box(data)
            results.append(obj)
        return results

    @staticmethod
    async def _dumpKeys(dataobj):
        tablename = dataobj.__name__
        select_statement = f'SELECT id FROM {tablename};'
        cursor = await turbindo.database.execute_sql_statement(select_statement)
        results = []
        for record in await cursor.fetchall():
            results.append(record[0])
        return results
