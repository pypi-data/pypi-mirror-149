import inspect

# Tests are to implement BaseTest class. BaseTest defines three functions:
# invoke_testcase, run_all_test_cases, and _get_case.
#
import os
from os.path import exists

from turbindo.configuration import TurbindoConfiguration
from turbindo.database import initialize_database
from turbindo.test.data import classes as test_dataclasses


class BaseTest:
    # _get_case:
    def __init__(self):
        self.dataclasses = test_dataclasses

    async def async_init(self):
        if exists('testdb.db'):
            os.remove('testdb.db')
        await initialize_database(TurbindoConfiguration().config, 'testdb.db', self.dataclasses)

    async def pre_test_setup(self):
        if exists('testdb.db'):
            os.remove('testdb.db')
        await initialize_database(TurbindoConfiguration().config, 'testdb.db', self.dataclasses)

    async def post_test_teardown(self):
        os.remove('testdb.db')

    def _get_case(self, name):
        for element in dir(self):
            if not element.startswith("__"):
                if callable(element):
                    if inspect.iscoroutinefunction(name):
                        getattr(self, name, element)

    async def invoke_testcase(self, name):
        case = self._get_case(name)

        try:
            result = await case()

        except:
            return False

        return result

    # run_all_testcases -- unimplemented
    async def run_all_testcases(self):
        pass
