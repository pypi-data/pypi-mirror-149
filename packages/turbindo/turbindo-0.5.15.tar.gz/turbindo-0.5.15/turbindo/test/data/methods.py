from typing import List

from turbindo.database.impl.sqlite.methods import execute_sql_statement

from turbindo.database.default.classes import IORecording
from turbindo.test import data as db
from turbindo.database.default.methods import condSelect


async def getAllTestRecordings() -> List[IORecording]:
    query = 'select id from IORecording'
    cursor = await execute_sql_statement(query)
    results = []
    for item in await cursor.fetchall():
        results.append(await db.readIORecording(item[0]))
    return results
