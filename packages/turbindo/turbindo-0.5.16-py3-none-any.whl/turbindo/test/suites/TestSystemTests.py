from turbindo.configuration import TurbindoConfiguration
from turbindo.test.base_test import BaseTest
from turbindo.log.logger import Logger


class TestSystemTests(BaseTest):
    EXPECTED_FAIL = ["test_failure_exc", "test_failure_retval"]

    def __init__(self):
        super().__init__()
        self.logger = Logger(self.__class__.__name__)

    async def test_failure_exc(self):
        raise Exception("this test should fail")

    async def test_failure_retval(self):
        return False

    async def test_pass(self):
        self.logger.log("pass test")
        return True
