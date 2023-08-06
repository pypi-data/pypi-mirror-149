import asyncio.queues

from turbindo.runtime.scheduler import OneShotTask, TaskContext, register_oneshot, run_oneshots, SchedulerState
from turbindo.test.base_test import BaseTest


class TestTasks(BaseTest):
    def __init__(self):
        super().__init__()

    async def test_oneshot_task(self) -> bool:
        ctx = TaskContext()
        q = asyncio.queues.Queue(maxsize=1)
        ctx.set("queue", q)
        await SchedulerState.setup()
        await register_oneshot(ShouldRunOnce(ctx=ctx, background=False))
        await run_oneshots()
        assert await q.get()
        return True


class ShouldRunOnce(OneShotTask):
    async def run(self):
        q: asyncio.Queue = self.ctx.get('queue')
        await q.put(True)
