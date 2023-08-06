from collections.abc import AsyncIterator
from typing import List

from aiosqlite import Cursor

from turbindo.database import Sqlite


async def sqllite_insert_into_table(sql_insert_statement, *params) -> Cursor:
    cursor = await Sqlite.conn.execute(sql_insert_statement, *params)
    await Sqlite.conn.commit()
    return cursor


async def sqlite_select_many(query, params) -> List[dict]:
    cursor = await Sqlite.conn.execute(query, params)
    names = list(map(lambda x: x[0], cursor.description))
    data: List[dict] = []
    for record in await cursor.fetchall():
        dict = {}
        for i in range(0, len(names)):
            dict[names[i]] = record[i]
        data.append(dict)
    return data


async def sqllite_select_from_table(sql_select, id=None):
    if id is None:
        params = []
    else:
        params = [id]

    cursor = await Sqlite.conn.execute(sql_select, params)

    names = list(map(lambda x: x[0], cursor.description))
    row = await cursor.fetchone()

    selected_row = row

    while row is not None:
        row = await cursor.fetchone()
        if (row is not None):
            selected_row = row

    return (selected_row, names)
