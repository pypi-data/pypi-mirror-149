import json

from turbindo.database.base_object import AbstractDataTable, BaseMachineData, TableMetaData


class IORecording(AbstractDataTable):
    metadata = TableMetaData()

    @property
    def start_time(self) -> int:
        return self.start_time

    @property
    def return_time(self) -> int:
        return self.data.return_time

    @property
    def return_value(self) -> str:
        return self.data.return_value

    @property  # catch, store, rethrow
    def exception(self) -> str:
        return self.data.exception

    @property
    def arg_hash(self) -> str:
        return self.data.arg_hash

    @property
    def fn(self) -> str:
        return self.data.fn

    @property
    def kwargs(self) -> dict:
        return json.loads(self.data.kwargs)

    @property
    def args(self) -> list:
        return json.loads(self.data.args)


class User(AbstractDataTable):
    metadata = TableMetaData()

    @property
    def name(self) -> str:
        return self.data.name

    @property
    def pubk(self) -> str:
        return self.data.pubk

    @property
    def email(self) -> str:
        return self.data.email

    @property
    def tennant(self) -> str:
        return self.data.tennant

    @property
    def pwhash(self) -> str:
        return self.data.pwhash

    @property
    def role(self) -> str:
        return self.data.role

    @property
    def pwsalt(self) -> str:
        return self.data.pwsalt

    @property
    def admin(self) -> bool:
        return self.data.admin


class MetaData(AbstractDataTable):
    @property
    def databaseVersion(self) -> int:
        return self.data.result


class TestResults(AbstractDataTable):
    @property
    def result(self) -> bool:
        return self.data.result

    @property
    def suite(self) -> str:
        return self.data.suite

    @property
    def test_case(self) -> str:
        return self.data.case

    @property
    def time(self) -> int:
        return self.data.testTime

    @property
    def exception(self) -> str:
        return self.data.exception


class ConsoleHistory(AbstractDataTable):

    @property
    def cmd(self) -> str:
        return self.data.cmd

    @property
    def args(self) -> list:
        return json.loads(self.data.args)

    @property
    def user_id(self) -> str:
        return self.data.user_id

    @property
    def cmd_exc_time(self) -> int:
        return self.data.cmd_exc_time

    @property
    def cmd_ret_time(self) -> int:
        return self.data.cmd_ret_time

    @property
    def success(self) -> bool:
        return self.data.success

    @property
    def exception(self) -> str:
        return self.data.exception

    @property
    def started(self) -> int:
        return self.data.started

    @property
    def finished(self) -> int:
        return self.data.finished


class MachineLog(BaseMachineData):
    # implicit state field inherited

    @property
    def transition_time(self) -> int:
        return self.data.transition_time

    # id of machine instance being logged
    @property
    def machine_inst_id(self) -> str:
        return self.data.machine_inst_id


class TaskHistory(AbstractDataTable):

    @property
    def task_name(self) -> str:
        return self.data.task_name

    @property
    def args(self) -> list:
        return json.loads(self.data.args)

    @property
    def task_exc_time(self) -> int:
        return self.data.cmd_exc_time

    @property
    def task_ret_time(self) -> int:
        return self.data.cmd_ret_time

    @property
    def success(self) -> bool:
        return self.data.success

    @property
    def exception(self) -> str:
        return self.data.exception

    @property
    def one_shot(self) -> bool:
        return self.data.one_shot
