from aiosqlite import Cursor

from turbindo.database import Sqlite
from turbindo.runtime.exceptions import NoRowFoundException


async def execute_sql_statement(sql_statement, *params) -> Cursor:
    # this fn only supports single statements
    assert sql_statement.count(';') < 2
    cursor = await Sqlite.conn.execute(sql_statement, *params)
    await Sqlite.conn.commit()
    return cursor


async def select_from_table(sql_select, primary_key=None):
    if primary_key is None:
        params = []
    else:
        params = [primary_key]

    if params.__len__() > 0:
        cursor = await Sqlite.conn.execute(sql_select, params)
    else:
        cursor = await Sqlite.conn.execute(sql_select)

    names = list(map(lambda x: x[0], cursor.description))
    row = await cursor.fetchone()
    if row is None:
        raise NoRowFoundException(f"no rows found for sql statement {sql_select}, primary key {primary_key}")

    return row, names