from asyncio import BaseEventLoop
from concurrent.futures import ThreadPoolExecutor
from turbindo.runtime.instrumented_object import InstrumentedIO, RecordedIO


class IOContext:
    loop: BaseEventLoop = None
    pool: ThreadPoolExecutor = None
    ioclass_instances = {}

    @classmethod
    def init(cls, loop, pool):
        cls.loop = loop
        cls.pool = pool

    @classmethod
    async def register(cls, target_class, recording=False, mocking=False):
        inst: InstrumentedIO = await target_class().async_init(cls.loop, cls.pool)

        if recording:
            cls.ioclass_instances[target_class.__name__] = await RecordedIO(inst).async_init(cls.loop,cls.pool)
        else:
            cls.ioclass_instances[target_class.__name__] = inst
    @classmethod
    def lookup(cls, target_class):
        return cls.ioclass_instances[target_class.__name__]
