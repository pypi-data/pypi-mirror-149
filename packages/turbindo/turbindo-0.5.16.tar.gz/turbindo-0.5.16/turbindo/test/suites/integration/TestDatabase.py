import os
import random
from typing import List
import uuid
import tempfile
from turbindo.configuration import TurbindoConfiguration
from turbindo.database import run_database_updates
from turbindo.test import data as db
from turbindo.util import TemporaryFile
from turbindo.database.preloader import Preloader
from turbindo.log.logger import Logger
from turbindo.runtime.exceptions import NoRowFoundException
from turbindo.test.base_test import BaseTest
from turbindo.test.data import TestcaseTable
from turbindo.database import initialize_database
from turbindo.test.data import classes as dataclasses

preload_data = """
TestcaseTable:
  one_test:
    dict_type:
      this: that
      some: other
    list_type: [ 1,2,3,4 ]
    a: "a"
    b: 1
  two_test:
    dict_type:
      a: b
      c: d
    list_type: [ 5,6,7,8 ]
    a: "b"
    b: 2
  three_test:
    list_type: [ "a" ]
    a: "c"
    b: 3
"""
class TestDatabase(BaseTest):
    def __init__(self):
        super().__init__()
        self.logger = Logger(self.__class__.__name__)
        self.config = TurbindoConfiguration().config

    async def async_init(self):
        await initialize_database(TurbindoConfiguration().config, 'testdb.db', dataclasses)

    async def pre_test_setup(self):
        await initialize_database(TurbindoConfiguration().config, 'testdb.db', dataclasses)

    async def post_test_teardown(self):
        os.remove('testdb.db')

    async def test_cond_select(self) -> bool:
        preload_test_data = TemporaryFile(preload_data)

        dp = Preloader(preload_test_data.file_path, db)
        await dp.run()
        results: List[TestcaseTable] = await db.condSelect(TestcaseTable, "b < 3")
        assert len(results) == 2
        for x in results:
            self.logger.debug(x.b)
            assert x.b < 4
        return True

    async def test_db_init(self) -> bool:
        updates = TemporaryFile("""
2:
  - create table SyntheticTable(id INTEGER PRIMARY KEY)
3:
  - alter table SyntheticTable ADD anewproperty text;
""")

        await run_database_updates(updates.file_path)
        updates.dispose()
        return True

    async def test_encodeings(self) -> bool:
        jsontestlist = ["Ford", "BMW", "Fiat"]
        jsontestdict = {"name": "John"}
        await db.writeTestcaseTable("1", dict_type=jsontestdict, list_type=jsontestlist)
        result = await db.readTestcaseTable("1")
        assert result.dict_type == jsontestdict
        assert result.list_type == jsontestlist
        return True

    async def test_preloader(self) -> bool:
        preload_test_data = TemporaryFile(preload_data)
        dp = Preloader(preload_test_data.file_path, db)
        await dp.run()
        return True

    async def test_read_write(self) -> bool:
        rando_id = random.randint(100, 10000)
        admin = False
        email = 'nobody@nowhere.lol'
        name = 'test_case'
        pubk = '12345'
        pwhash = '0abce'
        pwsalt = '12345'
        role = 'test_role'
        tennant = 'test_tennant'
        await db.writeUser(str(rando_id),
                           admin=admin,
                           email=email,
                           name=name,
                           pubk=pubk,
                           pwhash=pwhash,
                           pwsalt=pwsalt,
                           role=role,
                           tennant=tennant)
        read_value = await db.readUser(rando_id)
        assert read_value.id == str(rando_id)
        assert read_value.admin == admin
        assert read_value.email == email
        assert read_value.name == name
        assert read_value.pubk == pubk
        assert read_value.pwhash == pwhash
        assert read_value.pwsalt == pwsalt
        assert read_value.role == role
        assert read_value.tennant == tennant

        # delete the user row
        await db.deleteUser(rando_id)
        try:
            await db.readUser(rando_id)
        except NoRowFoundException as e:
            # if reading the non-existant user fails, we pass the test
            return True
        # otherwise we fail
        return False
