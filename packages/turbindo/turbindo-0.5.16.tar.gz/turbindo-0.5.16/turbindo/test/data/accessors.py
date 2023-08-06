#CODE GENERATED -- FILE DO NOT MODIFY

from typing import AsyncIterator, List

from turbindo.database.base_object import SPECIAL_TYPES
from turbindo.std.streams.stream import Stream



from turbindo.test.data.classes import BaseMachineData

from turbindo.test.data.classes import ConsoleHistory

from turbindo.test.data.classes import DoughnutMachineData

from turbindo.test.data.classes import IORecording

from turbindo.test.data.classes import MachineLog

from turbindo.test.data.classes import MetaData

from turbindo.test.data.classes import TaskHistory

from turbindo.test.data.classes import TestResults

from turbindo.test.data.classes import TestcaseTable

from turbindo.test.data.classes import User



async def readBaseMachineData(id) -> BaseMachineData:
  return await BaseMachineData(id).read()

async def writeBaseMachineData(id, state:str=SPECIAL_TYPES.NOT_SET) -> BaseMachineData:
  return await BaseMachineData(id).set(state=state)

async def deleteBaseMachineData(id):
  return await BaseMachineData(id).delete()

async def iterateBaseMachineData() -> AsyncIterator[BaseMachineData]:
  raise Exception("unimplemented")

async def dumpAllBaseMachineData() -> List[BaseMachineData]:
  return await BaseMachineData.dumpAll()

async def iterateKeysBaseMachineData() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysBaseMachineData() -> List[str]:
  return await BaseMachineData.dumpAllKeys()

async def clearAllBaseMachineData():
  return await BaseMachineData.truncate()

async def streamBaseMachineData() -> Stream:
  raise Exception("unimplemented")

async def selectBaseMachineDataWhere( state:str=SPECIAL_TYPES.NOT_SET) -> List[BaseMachineData]:
  return await BaseMachineData.selectWhere(state=state)

async def readConsoleHistory(id) -> ConsoleHistory:
  return await ConsoleHistory(id).read()

async def writeConsoleHistory(id, args:list=SPECIAL_TYPES.NOT_SET, cmd:str=SPECIAL_TYPES.NOT_SET, cmd_exc_time:int=SPECIAL_TYPES.NOT_SET, cmd_ret_time:int=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, finished:int=SPECIAL_TYPES.NOT_SET, started:int=SPECIAL_TYPES.NOT_SET, success:bool=SPECIAL_TYPES.NOT_SET, user_id:str=SPECIAL_TYPES.NOT_SET) -> ConsoleHistory:
  return await ConsoleHistory(id).set(args=args, cmd=cmd, cmd_exc_time=cmd_exc_time, cmd_ret_time=cmd_ret_time, exception=exception, finished=finished, started=started, success=success, user_id=user_id)

async def deleteConsoleHistory(id):
  return await ConsoleHistory(id).delete()

async def iterateConsoleHistory() -> AsyncIterator[ConsoleHistory]:
  raise Exception("unimplemented")

async def dumpAllConsoleHistory() -> List[ConsoleHistory]:
  return await ConsoleHistory.dumpAll()

async def iterateKeysConsoleHistory() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysConsoleHistory() -> List[str]:
  return await ConsoleHistory.dumpAllKeys()

async def clearAllConsoleHistory():
  return await ConsoleHistory.truncate()

async def streamConsoleHistory() -> Stream:
  raise Exception("unimplemented")

async def selectConsoleHistoryWhere( args:list=SPECIAL_TYPES.NOT_SET, cmd:str=SPECIAL_TYPES.NOT_SET, cmd_exc_time:int=SPECIAL_TYPES.NOT_SET, cmd_ret_time:int=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, finished:int=SPECIAL_TYPES.NOT_SET, started:int=SPECIAL_TYPES.NOT_SET, success:bool=SPECIAL_TYPES.NOT_SET, user_id:str=SPECIAL_TYPES.NOT_SET) -> List[ConsoleHistory]:
  return await ConsoleHistory.selectWhere(args=args, cmd=cmd, cmd_exc_time=cmd_exc_time, cmd_ret_time=cmd_ret_time, exception=exception, finished=finished, started=started, success=success, user_id=user_id)

async def readDoughnutMachineData(id) -> DoughnutMachineData:
  return await DoughnutMachineData(id).read()

async def writeDoughnutMachineData(id, donutometer:int=SPECIAL_TYPES.NOT_SET, dough_level:int=SPECIAL_TYPES.NOT_SET, filling_level:int=SPECIAL_TYPES.NOT_SET, service_time:int=SPECIAL_TYPES.NOT_SET, state:str=SPECIAL_TYPES.NOT_SET) -> DoughnutMachineData:
  return await DoughnutMachineData(id).set(donutometer=donutometer, dough_level=dough_level, filling_level=filling_level, service_time=service_time, state=state)

async def deleteDoughnutMachineData(id):
  return await DoughnutMachineData(id).delete()

async def iterateDoughnutMachineData() -> AsyncIterator[DoughnutMachineData]:
  raise Exception("unimplemented")

async def dumpAllDoughnutMachineData() -> List[DoughnutMachineData]:
  return await DoughnutMachineData.dumpAll()

async def iterateKeysDoughnutMachineData() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysDoughnutMachineData() -> List[str]:
  return await DoughnutMachineData.dumpAllKeys()

async def clearAllDoughnutMachineData():
  return await DoughnutMachineData.truncate()

async def streamDoughnutMachineData() -> Stream:
  raise Exception("unimplemented")

async def selectDoughnutMachineDataWhere( donutometer:int=SPECIAL_TYPES.NOT_SET, dough_level:int=SPECIAL_TYPES.NOT_SET, filling_level:int=SPECIAL_TYPES.NOT_SET, service_time:int=SPECIAL_TYPES.NOT_SET, state:str=SPECIAL_TYPES.NOT_SET) -> List[DoughnutMachineData]:
  return await DoughnutMachineData.selectWhere(donutometer=donutometer, dough_level=dough_level, filling_level=filling_level, service_time=service_time, state=state)

async def readIORecording(id) -> IORecording:
  return await IORecording(id).read()

async def writeIORecording(id, arg_hash:str=SPECIAL_TYPES.NOT_SET, args:list=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, fn:str=SPECIAL_TYPES.NOT_SET, kwargs:dict=SPECIAL_TYPES.NOT_SET, return_time:int=SPECIAL_TYPES.NOT_SET, return_value:str=SPECIAL_TYPES.NOT_SET, start_time:int=SPECIAL_TYPES.NOT_SET) -> IORecording:
  return await IORecording(id).set(arg_hash=arg_hash, args=args, exception=exception, fn=fn, kwargs=kwargs, return_time=return_time, return_value=return_value, start_time=start_time)

async def deleteIORecording(id):
  return await IORecording(id).delete()

async def iterateIORecording() -> AsyncIterator[IORecording]:
  raise Exception("unimplemented")

async def dumpAllIORecording() -> List[IORecording]:
  return await IORecording.dumpAll()

async def iterateKeysIORecording() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysIORecording() -> List[str]:
  return await IORecording.dumpAllKeys()

async def clearAllIORecording():
  return await IORecording.truncate()

async def streamIORecording() -> Stream:
  raise Exception("unimplemented")

async def selectIORecordingWhere( arg_hash:str=SPECIAL_TYPES.NOT_SET, args:list=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, fn:str=SPECIAL_TYPES.NOT_SET, kwargs:dict=SPECIAL_TYPES.NOT_SET, return_time:int=SPECIAL_TYPES.NOT_SET, return_value:str=SPECIAL_TYPES.NOT_SET, start_time:int=SPECIAL_TYPES.NOT_SET) -> List[IORecording]:
  return await IORecording.selectWhere(arg_hash=arg_hash, args=args, exception=exception, fn=fn, kwargs=kwargs, return_time=return_time, return_value=return_value, start_time=start_time)

async def readMachineLog(id) -> MachineLog:
  return await MachineLog(id).read()

async def writeMachineLog(id, machine_inst_id:str=SPECIAL_TYPES.NOT_SET, state:str=SPECIAL_TYPES.NOT_SET, transition_time:int=SPECIAL_TYPES.NOT_SET) -> MachineLog:
  return await MachineLog(id).set(machine_inst_id=machine_inst_id, state=state, transition_time=transition_time)

async def deleteMachineLog(id):
  return await MachineLog(id).delete()

async def iterateMachineLog() -> AsyncIterator[MachineLog]:
  raise Exception("unimplemented")

async def dumpAllMachineLog() -> List[MachineLog]:
  return await MachineLog.dumpAll()

async def iterateKeysMachineLog() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysMachineLog() -> List[str]:
  return await MachineLog.dumpAllKeys()

async def clearAllMachineLog():
  return await MachineLog.truncate()

async def streamMachineLog() -> Stream:
  raise Exception("unimplemented")

async def selectMachineLogWhere( machine_inst_id:str=SPECIAL_TYPES.NOT_SET, state:str=SPECIAL_TYPES.NOT_SET, transition_time:int=SPECIAL_TYPES.NOT_SET) -> List[MachineLog]:
  return await MachineLog.selectWhere(machine_inst_id=machine_inst_id, state=state, transition_time=transition_time)

async def readMetaData(id) -> MetaData:
  return await MetaData(id).read()

async def writeMetaData(id, databaseVersion:int=SPECIAL_TYPES.NOT_SET) -> MetaData:
  return await MetaData(id).set(databaseVersion=databaseVersion)

async def deleteMetaData(id):
  return await MetaData(id).delete()

async def iterateMetaData() -> AsyncIterator[MetaData]:
  raise Exception("unimplemented")

async def dumpAllMetaData() -> List[MetaData]:
  return await MetaData.dumpAll()

async def iterateKeysMetaData() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysMetaData() -> List[str]:
  return await MetaData.dumpAllKeys()

async def clearAllMetaData():
  return await MetaData.truncate()

async def streamMetaData() -> Stream:
  raise Exception("unimplemented")

async def selectMetaDataWhere( databaseVersion:int=SPECIAL_TYPES.NOT_SET) -> List[MetaData]:
  return await MetaData.selectWhere(databaseVersion=databaseVersion)

async def readTaskHistory(id) -> TaskHistory:
  return await TaskHistory(id).read()

async def writeTaskHistory(id, args:list=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, one_shot:bool=SPECIAL_TYPES.NOT_SET, success:bool=SPECIAL_TYPES.NOT_SET, task_exc_time:int=SPECIAL_TYPES.NOT_SET, task_name:str=SPECIAL_TYPES.NOT_SET, task_ret_time:int=SPECIAL_TYPES.NOT_SET) -> TaskHistory:
  return await TaskHistory(id).set(args=args, exception=exception, one_shot=one_shot, success=success, task_exc_time=task_exc_time, task_name=task_name, task_ret_time=task_ret_time)

async def deleteTaskHistory(id):
  return await TaskHistory(id).delete()

async def iterateTaskHistory() -> AsyncIterator[TaskHistory]:
  raise Exception("unimplemented")

async def dumpAllTaskHistory() -> List[TaskHistory]:
  return await TaskHistory.dumpAll()

async def iterateKeysTaskHistory() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysTaskHistory() -> List[str]:
  return await TaskHistory.dumpAllKeys()

async def clearAllTaskHistory():
  return await TaskHistory.truncate()

async def streamTaskHistory() -> Stream:
  raise Exception("unimplemented")

async def selectTaskHistoryWhere( args:list=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, one_shot:bool=SPECIAL_TYPES.NOT_SET, success:bool=SPECIAL_TYPES.NOT_SET, task_exc_time:int=SPECIAL_TYPES.NOT_SET, task_name:str=SPECIAL_TYPES.NOT_SET, task_ret_time:int=SPECIAL_TYPES.NOT_SET) -> List[TaskHistory]:
  return await TaskHistory.selectWhere(args=args, exception=exception, one_shot=one_shot, success=success, task_exc_time=task_exc_time, task_name=task_name, task_ret_time=task_ret_time)

async def readTestResults(id) -> TestResults:
  return await TestResults(id).read()

async def writeTestResults(id, exception:str=SPECIAL_TYPES.NOT_SET, result:bool=SPECIAL_TYPES.NOT_SET, suite:str=SPECIAL_TYPES.NOT_SET, test_case:str=SPECIAL_TYPES.NOT_SET, time:int=SPECIAL_TYPES.NOT_SET) -> TestResults:
  return await TestResults(id).set(exception=exception, result=result, suite=suite, test_case=test_case, time=time)

async def deleteTestResults(id):
  return await TestResults(id).delete()

async def iterateTestResults() -> AsyncIterator[TestResults]:
  raise Exception("unimplemented")

async def dumpAllTestResults() -> List[TestResults]:
  return await TestResults.dumpAll()

async def iterateKeysTestResults() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysTestResults() -> List[str]:
  return await TestResults.dumpAllKeys()

async def clearAllTestResults():
  return await TestResults.truncate()

async def streamTestResults() -> Stream:
  raise Exception("unimplemented")

async def selectTestResultsWhere( exception:str=SPECIAL_TYPES.NOT_SET, result:bool=SPECIAL_TYPES.NOT_SET, suite:str=SPECIAL_TYPES.NOT_SET, test_case:str=SPECIAL_TYPES.NOT_SET, time:int=SPECIAL_TYPES.NOT_SET) -> List[TestResults]:
  return await TestResults.selectWhere(exception=exception, result=result, suite=suite, test_case=test_case, time=time)

async def readTestcaseTable(id) -> TestcaseTable:
  return await TestcaseTable(id).read()

async def writeTestcaseTable(id, a:str=SPECIAL_TYPES.NOT_SET, b:int=SPECIAL_TYPES.NOT_SET, dict_type:dict=SPECIAL_TYPES.NOT_SET, list_type:list=SPECIAL_TYPES.NOT_SET) -> TestcaseTable:
  return await TestcaseTable(id).set(a=a, b=b, dict_type=dict_type, list_type=list_type)

async def deleteTestcaseTable(id):
  return await TestcaseTable(id).delete()

async def iterateTestcaseTable() -> AsyncIterator[TestcaseTable]:
  raise Exception("unimplemented")

async def dumpAllTestcaseTable() -> List[TestcaseTable]:
  return await TestcaseTable.dumpAll()

async def iterateKeysTestcaseTable() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysTestcaseTable() -> List[str]:
  return await TestcaseTable.dumpAllKeys()

async def clearAllTestcaseTable():
  return await TestcaseTable.truncate()

async def streamTestcaseTable() -> Stream:
  raise Exception("unimplemented")

async def selectTestcaseTableWhere( a:str=SPECIAL_TYPES.NOT_SET, b:int=SPECIAL_TYPES.NOT_SET, dict_type:dict=SPECIAL_TYPES.NOT_SET, list_type:list=SPECIAL_TYPES.NOT_SET) -> List[TestcaseTable]:
  return await TestcaseTable.selectWhere(a=a, b=b, dict_type=dict_type, list_type=list_type)

async def readUser(id) -> User:
  return await User(id).read()

async def writeUser(id, admin:bool=SPECIAL_TYPES.NOT_SET, email:str=SPECIAL_TYPES.NOT_SET, name:str=SPECIAL_TYPES.NOT_SET, pubk:str=SPECIAL_TYPES.NOT_SET, pwhash:str=SPECIAL_TYPES.NOT_SET, pwsalt:str=SPECIAL_TYPES.NOT_SET, role:str=SPECIAL_TYPES.NOT_SET, tennant:str=SPECIAL_TYPES.NOT_SET) -> User:
  return await User(id).set(admin=admin, email=email, name=name, pubk=pubk, pwhash=pwhash, pwsalt=pwsalt, role=role, tennant=tennant)

async def deleteUser(id):
  return await User(id).delete()

async def iterateUser() -> AsyncIterator[User]:
  raise Exception("unimplemented")

async def dumpAllUser() -> List[User]:
  return await User.dumpAll()

async def iterateKeysUser() -> AsyncIterator[str]:
  raise Exception("unimplemented")

async def dumpAllKeysUser() -> List[str]:
  return await User.dumpAllKeys()

async def clearAllUser():
  return await User.truncate()

async def streamUser() -> Stream:
  raise Exception("unimplemented")

async def selectUserWhere( admin:bool=SPECIAL_TYPES.NOT_SET, email:str=SPECIAL_TYPES.NOT_SET, name:str=SPECIAL_TYPES.NOT_SET, pubk:str=SPECIAL_TYPES.NOT_SET, pwhash:str=SPECIAL_TYPES.NOT_SET, pwsalt:str=SPECIAL_TYPES.NOT_SET, role:str=SPECIAL_TYPES.NOT_SET, tennant:str=SPECIAL_TYPES.NOT_SET) -> List[User]:
  return await User.selectWhere(admin=admin, email=email, name=name, pubk=pubk, pwhash=pwhash, pwsalt=pwsalt, role=role, tennant=tennant)
