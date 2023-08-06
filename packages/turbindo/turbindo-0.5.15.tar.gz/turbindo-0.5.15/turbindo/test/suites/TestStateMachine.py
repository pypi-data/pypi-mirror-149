import os
import uuid

from turbindo.configuration import TurbindoConfiguration
from turbindo.database import initialize_database
from turbindo.log.logger import Logger
from turbindo.machine import TurbindoMachine
from turbindo.test import data as test_db
from turbindo.test.base_test import BaseTest
from turbindo.test.data import classes as test_data_classes, DoughnutMachineData


class TestStateMachine(BaseTest):
    def __init__(self):
        super().__init__()
        try:
            os.remove('testdb.db')
        except FileNotFoundError:
            pass
        self.logger = Logger(f"MachineTest")

    async def async_init(self):
        await initialize_database(TurbindoConfiguration().config, 'testdb.db', test_data_classes)

    async def test_construct_machine(self):
        dm = await DoughnutMachine(str(uuid.uuid4())).abuild()
        self.logger.log(f"from test dm.state: {dm.state}")
        await dm.start()
        for run in [1,2]:
            self.logger.log(f"from test dm.state: {dm.state}")
            await dm.lay()
            self.logger.log(f"from test dm.state: {dm.state}")
            await dm.fill()
            self.logger.log(f"from test dm.state: {dm.state}")
            await dm.bake()
            self.logger.log(f"from test dm.state: {dm.state}")
            await dm.deliver()
            self.logger.log(f"from test dm.state: {dm.state}")
            await dm.reset()
        self.logger.log(f"from test dm.state: {dm.state}")
        try:
            await dm.lay()
        except AssertionError as e:
            return True #out of dough
        return False


class DoughnutMachine(TurbindoMachine):
    TRAY_SIZE = 8

    def __init__(self, db_id):
        self.db_id = db_id
        # for type hints
        self.data: DoughnutMachineData = DoughnutMachineData(db_id)
        self.logger = Logger(f"DoughnutMachine {db_id}")
        state_list = ["off", "ready", "layed", "filled", "baked", "delivered", "out_of_filling", "out_of_dough",
                      "fault"]
        super().__init__(db_id, "off", state_list, test_db.readDoughnutMachineData, test_db.writeDoughnutMachineData)
        self.declare_transition("start", "off", "ready", [self.warmup], [])
        self.declare_transition("lay", "ready", "layed", [self.lay_doughnuts], [])
        self.declare_transition("no_dough", "ready", "out_of_dough", [self.lay_doughnuts], [])
        self.declare_transition("fill", "layed", "filled", [self.fill_doughnuts], [])
        self.declare_transition("no_filling", "layed", "out_of_filling", [self.no_filling_error], [])
        self.declare_transition("bake", "filled", "baked", [self.bake_doughnuts], [])
        self.declare_transition("deliver", "baked", "delivered", [self.deliver_doughnuts], [])
        self.declare_transition("fault", state_list, "fault", [self.handle_fault], [])
        self.declare_transition("reset", "delivered", "ready", [self.reset_machine], [])

    async def warmup(self):
        self.logger.log("warming up doughnut machine")
        self.logger.log(f"inside warmup self.state: {self.state}")

    async def lay_doughnuts(self):
        assert self.data.dough_level >= DoughnutMachine.TRAY_SIZE
        await test_db.writeDoughnutMachineData(self.db_id,
                                               dough_level=self.data.dough_level - DoughnutMachine.TRAY_SIZE)
        self.logger.log(f"inside lay self.state: {self.state}")

    async def fill_doughnuts(self):
        assert self.data.filling_level >= DoughnutMachine.TRAY_SIZE
        await test_db.writeDoughnutMachineData(self.db_id,
                                               filling_level=self.data.filling_level - DoughnutMachine.TRAY_SIZE)

    async def bake_doughnuts(self):
        self.logger.log("bake_doughnuts")

    async def deliver_doughnuts(self):
        self.logger.log("deliver_doughnuts")

    async def handle_fault(self):
        self.logger.log("handle_fault")

    async def no_filling_error(self):
        self.logger.log("no_filling_error")

    async def reset_machine(self):
        self.logger.log("reset machine")
