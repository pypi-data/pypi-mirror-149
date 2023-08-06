#CODE GENERATED -- FILE DO NOT MODIFY

from turbindo.database.base_object import SPECIAL_TYPES




from turbindo.database.default.classes import ConsoleHistory

from turbindo.database.default.classes import IORecording

from turbindo.database.default.classes import MetaData

from turbindo.database.default.classes import TaskHistory

from turbindo.database.default.classes import TestResults

from turbindo.test.data.classes import TestcaseTable

from turbindo.database.default.classes import User



async def readConsoleHistory(id) -> ConsoleHistory:
  return await ConsoleHistory(id).read()

async def writeConsoleHistory(id, args:list=SPECIAL_TYPES.NOT_SET, cmd:str=SPECIAL_TYPES.NOT_SET, cmd_exc_time:int=SPECIAL_TYPES.NOT_SET, cmd_ret_time:int=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, finished:int=SPECIAL_TYPES.NOT_SET, started:int=SPECIAL_TYPES.NOT_SET, success:bool=SPECIAL_TYPES.NOT_SET, user_id:str=SPECIAL_TYPES.NOT_SET) -> ConsoleHistory:
  return await ConsoleHistory(id).set(args=args, cmd=cmd, cmd_exc_time=cmd_exc_time, cmd_ret_time=cmd_ret_time, exception=exception, finished=finished, started=started, success=success, user_id=user_id)

async def deleteConsoleHistory(id):
  return await ConsoleHistory(id).delete()

async def readIORecording(id) -> IORecording:
  return await IORecording(id).read()

async def writeIORecording(id, arg_hash:str=SPECIAL_TYPES.NOT_SET, args:list=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, fn:str=SPECIAL_TYPES.NOT_SET, kwargs:dict=SPECIAL_TYPES.NOT_SET, return_time:int=SPECIAL_TYPES.NOT_SET, return_value:str=SPECIAL_TYPES.NOT_SET, start_time:int=SPECIAL_TYPES.NOT_SET) -> IORecording:
  return await IORecording(id).set(arg_hash=arg_hash, args=args, exception=exception, fn=fn, kwargs=kwargs, return_time=return_time, return_value=return_value, start_time=start_time)

async def deleteIORecording(id):
  return await IORecording(id).delete()

async def readMetaData(id) -> MetaData:
  return await MetaData(id).read()

async def writeMetaData(id, databaseVersion:int=SPECIAL_TYPES.NOT_SET) -> MetaData:
  return await MetaData(id).set(databaseVersion=databaseVersion)

async def deleteMetaData(id):
  return await MetaData(id).delete()

async def readTaskHistory(id) -> TaskHistory:
  return await TaskHistory(id).read()

async def writeTaskHistory(id, args:list=SPECIAL_TYPES.NOT_SET, exception:str=SPECIAL_TYPES.NOT_SET, one_shot:bool=SPECIAL_TYPES.NOT_SET, success:bool=SPECIAL_TYPES.NOT_SET, task_exc_time:int=SPECIAL_TYPES.NOT_SET, task_name:str=SPECIAL_TYPES.NOT_SET, task_ret_time:int=SPECIAL_TYPES.NOT_SET) -> TaskHistory:
  return await TaskHistory(id).set(args=args, exception=exception, one_shot=one_shot, success=success, task_exc_time=task_exc_time, task_name=task_name, task_ret_time=task_ret_time)

async def deleteTaskHistory(id):
  return await TaskHistory(id).delete()

async def readTestResults(id) -> TestResults:
  return await TestResults(id).read()

async def writeTestResults(id, exception:str=SPECIAL_TYPES.NOT_SET, result:bool=SPECIAL_TYPES.NOT_SET, suite:str=SPECIAL_TYPES.NOT_SET, test_case:str=SPECIAL_TYPES.NOT_SET, time:int=SPECIAL_TYPES.NOT_SET) -> TestResults:
  return await TestResults(id).set(exception=exception, result=result, suite=suite, test_case=test_case, time=time)

async def deleteTestResults(id):
  return await TestResults(id).delete()

async def readTestcaseTable(id) -> TestcaseTable:
  return await TestcaseTable(id).read()

async def writeTestcaseTable(id, dict_type:dict=SPECIAL_TYPES.NOT_SET, list_type:list=SPECIAL_TYPES.NOT_SET) -> TestcaseTable:
  return await TestcaseTable(id).set(dict_type=dict_type, list_type=list_type)

async def deleteTestcaseTable(id):
  return await TestcaseTable(id).delete()

async def readUser(id) -> User:
  return await User(id).read()

async def writeUser(id, admin:bool=SPECIAL_TYPES.NOT_SET, email:str=SPECIAL_TYPES.NOT_SET, name:str=SPECIAL_TYPES.NOT_SET, pubk:str=SPECIAL_TYPES.NOT_SET, pwhash:str=SPECIAL_TYPES.NOT_SET, pwsalt:str=SPECIAL_TYPES.NOT_SET, role:str=SPECIAL_TYPES.NOT_SET, tennant:str=SPECIAL_TYPES.NOT_SET) -> User:
  return await User(id).set(admin=admin, email=email, name=name, pubk=pubk, pwhash=pwhash, pwsalt=pwsalt, role=role, tennant=tennant)

async def deleteUser(id):
  return await User(id).delete()
