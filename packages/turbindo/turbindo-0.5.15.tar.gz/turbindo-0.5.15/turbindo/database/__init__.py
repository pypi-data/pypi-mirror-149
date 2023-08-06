import numbers
from typing import List

import aiosqlite
import yaml
from jinja2 import Template

import turbindo.database.base_object
from turbindo.database.base_object import AbstractDataTable
from turbindo.database.impl.sqlite import Sqlite, sqlite_type_rev_lookup
from turbindo.database.impl.sqlite.SqliteDataTable import SqliteDataTable
from turbindo.database.base_object import TableMetaData
# from turbindo.database.default.data_objects import TestResults, MetaData
from turbindo.database.impl.sqlite.methods import execute_sql_statement, select_from_table
from turbindo.database.default.classes import MetaData
from turbindo.log.logger import Logger
from turbindo.runtime.exceptions import NoRowFoundException
from turbindo.util import get_ondisk_type_map, get_package_classes

logger = Logger(__file__)

schema_version = 2


def create_table_def(clazz):
    if not issubclass(clazz, AbstractDataTable):
        raise Exception(f"{clazz.__name__} does not extendAbstractDataTable")

    field_type_map = get_ondisk_type_map(clazz)

    field_type_map.pop('id')

    def emit_default(clazz: type, field) -> str:
        meta: TableMetaData = getattr(clazz, "metadata")
        if field not in meta.default_values:
            return ""
        if isinstance(meta.default_values[field], numbers.Number):
            return f"DEFAULT {meta.default_values[field]}"
        return f"DEFAULT '{meta.default_values[field]}'"

    def emit_unique(clazz: type) -> str:
        meta: TableMetaData = getattr(clazz, "metadata")
        if meta.unique_fields:
            return f',UNIQUE({",".join(meta.unique_fields)})'
        return ''

    create_table_template = Template(
        """
        CREATE TABLE IF NOT EXISTS   {{ table_name }}   ( 
        {% for name, type in fields.items() -%} 
        {{ name }} {{type}} {{ emit_default(clazz, name) }},
        {% endfor -%} 
        id TEXT
        {{ emit_unique(clazz) }}
        );
        """
    )
    create_table_template.globals['emit_default'] = emit_default
    create_table_template.globals['emit_unique'] = emit_unique

    rendered_string = create_table_template.render(table_name=clazz.__name__,
                                                   fields=field_type_map,
                                                   clazz=clazz)

    return rendered_string


async def create_connection_sqlite(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = await aiosqlite.connect(db_file)
    return conn


async def get_columns_from_table(sql_select) -> List[str]:
    cursor = await Sqlite.conn.execute(sql_select)
    names = list(map(lambda x: x[0], cursor.description))
    return names


async def run_schema_updates(yamlfile):
    sql_select_max_version = """ SELECT max(databaseVersion ) FROM MetaData """

    try:
        max_ver_row, names = await select_from_table(sql_select_max_version)
        if (max_ver_row is not None):
            if (max_ver_row[0] is not None):
                max_ver_from_db = int(max_ver_row[0])
            else:
                max_ver_from_db = 0
    except NoRowFoundException as e:
        max_ver_from_db = 0

    with open(yamlfile) as f:
        updatesDoc = yaml.load_all(f, Loader=yaml.FullLoader)

        master_update_sql_statement_TMPL = Template(
            "INSERT INTO MetaData (databaseVersion) VALUES({{db_version}})")

        async def do_update(sqlStatement):
            versFromFile = int(theUpdateNumber)
            if versFromFile > max_ver_from_db:
                # update database with sql query from file
                sql_statement_to_execute = sqlStatement
                await execute_sql_statement(sql_statement_to_execute)

                # add updated version to database
                master_update_sql_statement = master_update_sql_statement_TMPL.render(
                    db_version=versFromFile)
                await execute_sql_statement(
                    master_update_sql_statement)

        for doc in updatesDoc:
            for theUpdateNumber, entry in doc.items():
                if type(entry) is list:
                    for sqlStatement in entry:
                        await do_update(sqlStatement)
                else:
                    await do_update(entry)


async def run_database_updates(yaml_file):
    await run_schema_updates(yaml_file)


async def initialize_metadata():
    create_meta_data_sql = create_table_def(MetaData)
    await execute_sql_statement(create_meta_data_sql)

    try:
        await select_from_table("select * from MetaData")
    except NoRowFoundException:
        await execute_sql_statement("insert into MetaData (databaseVersion) values (1)")


async def select_from_table_into_dictionary(sql_select, id=None):
    if id is None:
        params = []
    else:
        params = [id]

    cursor = await Sqlite.conn.execute(sql_select, params)
    names = list(map(lambda x: x[0], cursor.description))

    row = await cursor.fetchone()

    all_rows_list = []

    while row is not None:
        results_dictionary = {}
        for i in range(names.__len__()):
            results_dictionary[names[i]] = row[i]

        all_rows_list.append(results_dictionary.copy())

        row = await cursor.fetchone()

    return all_rows_list


async def initialize_database(config, disk_path, data_class_package):
    if config.db.driver == 'sqlite':
        base_object.AbstractDataTable.DATABASE_IMPL = SqliteDataTable
        return await initialize_database_sqlite(disk_path, data_class_package)


async def initialize_database_sqlite(file_path, data_class_package):
    Sqlite.conn = await aiosqlite.connect(file_path)
    assert Sqlite.conn.is_alive()
    await initialize_metadata()
    package_classes = get_package_classes(data_class_package,
                                          ["DataTable", "AbstractDataTable"],
                                          turbindo.database.base_object.AbstractDataTable)

    class_sql_statements = []

    if package_classes.__len__() == 0:
        raise Exception("no data classes found")
    else:
        for cls in package_classes:
            sql_create = create_table_def(cls)
            class_sql_statements.append(sql_create)
        if (class_sql_statements.__len__() > 0):
            for statement in class_sql_statements:
                await execute_sql_statement(statement)
