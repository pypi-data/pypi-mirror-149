from __future__ import annotations


# inherit from UserList?

class Stream:
    async def next(self):
        pass

    async def parallel(self) -> Stream:
        pass

    async def map(self, fn) -> Stream:
        pass

    async def filter(self, fn) -> Stream:
        pass

    async def foreach(self, fn) -> None:
        pass

    def __getitem__(self, item):
        pass


class ParallelStream(Stream):
    pass
