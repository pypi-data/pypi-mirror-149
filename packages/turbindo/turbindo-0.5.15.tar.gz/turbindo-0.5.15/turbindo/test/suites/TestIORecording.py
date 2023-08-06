import os
from typing import List

from turbindo.configuration import TurbindoConfiguration
from turbindo.database import initialize_database
from turbindo.database.default import IORecording
from turbindo.log.logger import Logger
from turbindo.test.base_test import BaseTest
from turbindo.test.data import classes as test_data_classes
from turbindo.test import data as test_db
from turbindo.test import io as test_io
from turbindo.test.io import DoughnutPrinter


class TestIORecording(BaseTest):
    def __init__(self):
        super().__init__()
        try:
            os.remove('testdb.db')
        except FileNotFoundError:
            pass
        self.logger = Logger(f"MachineTest")

    async def async_init(self):
        await initialize_database(TurbindoConfiguration().config, 'testdb.db', test_data_classes)
        await test_io.setup(recording=[DoughnutPrinter])

    async def test_record_io_call(self):
        await test_db.clearAllIORecording()
        arg_1 = 1
        res1 = await test_io.dough().extrude_dough(arg_1)
        # async for rec in test_db.iterateIORecording(where=lambda rec: rec.id != 'abc')
        recordings: List[IORecording] = await test_db.getAllTestRecordings()
        print(recordings[0].fn)
        assert recordings[0].args[0] == arg_1
        return True
