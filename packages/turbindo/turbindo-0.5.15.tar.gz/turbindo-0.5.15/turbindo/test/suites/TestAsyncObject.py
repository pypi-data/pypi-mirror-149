from turbindo.log.logger import Logger
from turbindo.runtime.io_context import IOContext
from turbindo.runtime.instrumented_object import InstrumentedIO
from turbindo.test.base_test import BaseTest


class TestAsyncObject(BaseTest):
    async def test_io(self) -> bool:
        await IOContext.register(TestClass)
        test_wrapped_obj: TestClass = IOContext.lookup(TestClass)
        await test_wrapped_obj.test1()
        await test_wrapped_obj.test2()
        return True

    async def test_t1(self) -> bool:
        await IOContext.register(TestClass)
        test_wrapped_obj: TestClass = IOContext.lookup(TestClass)
        await test_wrapped_obj.test1()
        return True


class TestClass(InstrumentedIO):
    def __init__(self):
        self.logger = Logger(TestClass.__name__)

    def test1(self):
        self.logger.log("hello from within test1/async_object_test")
        return ("successful test1 call")

    async def test2(self):
        self.logger.log("hello from within test2/async_object_test")
        return "successful test2 call"
