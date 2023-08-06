from typing import List
from turbindo.database.impl.sqlite.methods import execute_sql_statement
from turbindo.database.default import accessors as default_accessors


async def condSelect(cls: type, clause: str, accessors=default_accessors) -> List:
    table = cls.__name__
    query = f"SELECT id FROM {table} WHERE " + clause
    cursor = await execute_sql_statement(query)
    getter = getattr(accessors, f"read{table}")
    results = []
    for item in await cursor.fetchall():
        results.append(await getter(item[0]))
    return results
