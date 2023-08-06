from turbindo.database.default.classes import *

class DoughnutMachineData(AbstractDataTable):
    metadata = TableMetaData(default_values={
        "dough_level": 16,
        "filling_level": 16
    })

    @property
    def state(self) -> str:
        return self.data.state

    @property
    def donutometer(self) -> int:
        return self.data.donutometer

    # @column_def(default=16)
    @property
    def dough_level(self) -> int:
        return self.data.dough_level

    @property
    def filling_level(self) -> int:
        return self.data.filling_level

    @property
    def service_time(self) -> int:
        return self.data.service_time


class TestcaseTable(AbstractDataTable):

    @property
    def dict_type(self) -> dict:
        return json.loads(self.data.dict_type)

    @property
    def list_type(self) -> list:
        return json.loads(self.data.list_type)

    @property
    def a(self) -> str:
        return self.data.a

    @property
    def b(self) -> int:
        return self.data.b
