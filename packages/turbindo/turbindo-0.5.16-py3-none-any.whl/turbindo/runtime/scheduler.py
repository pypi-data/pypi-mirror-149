import functools
from abc import abstractmethod
from typing import List, Type, Optional

import aiocron
import aiojobs
from aiojobs import Scheduler

from turbindo.util import get_ref_to_async_function


class SchedulerState:
    scheduler: Scheduler = None

    @classmethod
    async def setup(cls):
        SchedulerState.scheduler = await aiojobs.create_scheduler()


async def dispatch_job(job):
    await SchedulerState.scheduler.spawn(job)


async def setup_scheduler(schedule, tasks_package, sched_args={}):
    for fn_name, cronstr in schedule.items():
        fn_ref = await get_ref_to_async_function(tasks_package, fn_name)
        if fn_name in sched_args:
            _n = fn_ref.__name__
            args = sched_args[fn_name]
            fn_ref = functools.partial(fn_ref, *args)
            fn_ref.__name__ = _n
        setattr(fn_ref, '_is_coroutine', object())
        aiocron.crontab(cronstr, func=fn_ref, start=True)


class TaskContext:
    def __init__(self):
        self.ctx = {}

    def set(self, key, val):
        self.ctx[key] = val

    def get(self, key):
        return self.ctx[key]


class BaseTask:
    def __init__(self, ctx: TaskContext = TaskContext()):
        self.ctx = ctx

    @abstractmethod
    async def run(self):
        pass


class OneShotTask(BaseTask):
    def __init__(self, ctx: TaskContext = TaskContext(), background: bool = True):
        super().__init__(ctx=ctx)
        self.background = background


class TaskQueue:
    q: List[OneShotTask] = []
    sealed = False
    complete = False
    failures = {}


class CronTask(BaseTask):
    pass



async def register_oneshot(tsk: OneShotTask):
    TaskQueue.q.append(tsk)


async def run_oneshots():
    for tsk in TaskQueue.q:
        if tsk.background:
            await dispatch_job(tsk.run())
        else:
            await tsk.run()
