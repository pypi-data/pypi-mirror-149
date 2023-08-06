import asyncio
import functools
import hashlib
import uuid
from asyncio import BaseEventLoop
from functools import partial
import inspect
from traceback import format_exc
from typing import Callable, Dict
from turbindo.database import default as db
from turbindo.util import timestamp


class InstrumentedObject:
    def __init__(self, target_instance, loop: BaseEventLoop, pool):
        self.target_instance = target_instance
        self.loop = loop
        self.pool = pool
        self.wrapped_method_list = []


    async def async_init(self):
        self.target_instance = self.target_instance
        self.setup_instrumentation()
        return self

    def setup_instrumentation(self):
        for name in dir(self.target_instance):
            handle = getattr(self.target_instance, name)
            if not name.startswith("__"):
                if callable(handle):
                    if inspect.iscoroutinefunction(handle):
                        setattr(self, name, handle)
                        self.wrapped_method_list.append(name)
                    else:
                        setattr(self, name, partial(self.fn_wrapper, handle))
                        self.wrapped_method_list.append(name)


    async def fn_wrapper(self, fn, *args, **kwargs):
        loop = asyncio.get_event_loop()  # TODO why does passing the event loop error but this works
        fut = loop.run_in_executor(self.pool, functools.partial(fn, *args, **kwargs))
        result = await asyncio.wait_for(fut, None, loop=loop)
        return result


def hash_args(fn, *args, **kwargs):
    m = hashlib.sha1()
    m.update(bytes(fn.__name__,'UTF-8'))
    for arg in args:
        m.update(bytes(arg))
    for key, value in kwargs:
        m.update(bytes(key))
        m.update(bytes(value))
    return m.hexdigest()


def seralize_kwargs(**param):
    return param


def seralize_args(*param):
    return param


def seralize_return(ret):
    return str(ret)

#@todo make a recording mode that only records timeing data, or lets you mask pieces of data
class RecordedObject(InstrumentedObject):
    def __init__(self, target_instance, loop: BaseEventLoop, pool):
        super().__init__(target_instance, loop, pool)

    async def async_init(self):
        self.setup_recording()
        return self

    def setup_recording(self):
        for name in self.target_instance.wrapped_method_list:
            handle = getattr(self.target_instance, name)
            if not name.startswith("__"):
                if callable(handle):
                    if inspect.iscoroutinefunction(handle):
                        setattr(self, name, partial(self.recorded_fn_wrapper, handle))

    async def recorded_fn_wrapper(self, fn: callable, *args, **kwargs):
        arg_hash = hash_args(fn, *args, **kwargs)
        ser_args = seralize_args(*args)
        ser_kwargs = seralize_kwargs(**kwargs)
        record_id = str(uuid.uuid4())
        result = None
        await db.writeIORecording(record_id,
                                  arg_hash=arg_hash,
                                  fn=fn.__name__,
                                  args=list(ser_args),
                                  kwargs=dict(ser_kwargs),
                                  start_time=timestamp())
        try:
            result = await fn(*args, **kwargs)
        except Exception as e:
            await db.writeIORecording(record_id, exception=format_exc(), return_time=timestamp())
            raise e
        await db.writeIORecording(record_id, return_value=seralize_return(result), return_time=timestamp())
        return result


class MockedObject(InstrumentedObject):
    async def async_init(self):
        pass

    def setup_recording(self):
        for name in dir(self.target_instance):
            handle = getattr(self.target_instance, name)
            if not name.startswith("__"):
                if callable(handle):
                    if inspect.iscoroutinefunction(handle):
                        setattr(self, name, handle)
                    else:
                        setattr(self, name, partial(self.fn_wrapper, handle))

    async def mocked_fn_wrapper(self, fn, *args, **kwargs):
        pass


class InstrumentedIO:
    async def async_init(self, loop, pool):
        return await InstrumentedObject(self, loop, pool).async_init()


# should wrap an InstrumetedObject and record its return vals to a db table
class RecordedIO:
    def __init__(self, target: InstrumentedIO):
        self.target = target

    async def async_init(self, loop, pool):
        instrumented_obj = await self.target.async_init(loop, pool)
        recorded_obj = await RecordedObject(instrumented_obj, loop, pool).async_init()
        return recorded_obj


# should wrap an InstrumentedObject and lookup data from a table
# if the called fn is in result_transformers, the data read from the db is passed thru the registered fn
# if no data is available from the db, and a result_transformer is registered, it may return entirely synthetic data

class MockedIO(InstrumentedIO):
    def __init__(self, table_name: str, result_transformers: Dict[str, Callable]):
        pass
