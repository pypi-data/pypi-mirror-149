import json

from turbindo.database.base_object import AbstractDataTable


class TestDatabaseDefClass(AbstractDataTable):
    @property
    def remote(self) -> str:
        return self.data.remote

    @property
    def time(self) -> int:
        return self.data.time

    @property
    def args(self) -> list:
        return self.data.args

    @property
    def body(self) -> dict:
        return self.data.body


class TestDatabaseDefClass2(AbstractDataTable):
    @property
    def remote(self) -> str:
        return self.data.remote

    @property
    def time(self) -> int:
        return self.data.time

    @property
    def argszzz(self) -> list:

        return json.loads(self.data.argszzz)

    @property
    def body(self) -> dict:
        return json.loads(self.data.body)
