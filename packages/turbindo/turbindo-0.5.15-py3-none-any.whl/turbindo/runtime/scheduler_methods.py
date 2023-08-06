import datetime

import croniter

from turbindo.runtime.scheduler import SchedulerState


async def print_schedule():
    sched = {}
    for cron, args in SchedulerState.cron_list:
        ci: croniter.croniter = cron.croniter
        next = str(datetime.datetime.fromtimestamp(ci.get_next()))
        sched[cron.spec] = {"name": cron.func.__name__, "args": args, "next": next}
    return sched


async def print_time():
    return str(datetime.date.today())
