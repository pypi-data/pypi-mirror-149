import os
import uuid
import tempfile
import asyncio
import hashlib
import inspect
import json
import time

from turbindo.database.impl.sqlite import SQL_TYPE_LOOKUP
from turbindo.log.logger import Logger


async def noop(*args, **kwargs):
    pass


def hash_values(values: list) -> str:
    m = hashlib.sha256()
    for v in values:
        m.update(str(v).encode("UTF-8"))
    return m.hexdigest()


class TemporaryFile:
    def __init__(self, content):
        uid = uuid.uuid4()
        self.fp = f"{tempfile.gettempdir()}/{uid}"
        f = open(self.fp, 'w')
        f.write(content)
        f.flush()

    @property
    def file_path(self):
        return self.fp

    def dispose(self):
        os.remove(self.fp)


def kvdefault(dict, key, default):
    if key in dict:
        return dict[key]
    return default


def timestamp():
    return time.time()


def json_pretty(value):
    return json.dumps(value, indent=4, sort_keys=True)


def get_object_type_map(clazz) -> dict:
    properties = inspect.getmembers(clazz, lambda o: isinstance(o, property))
    field_type_map = {}
    for prop in properties:
        field_name = prop[0]
        field_type = inspect.signature(
            getattr(getattr(clazz, field_name), "fget"))
        field_type_str = field_type.return_annotation.__name__
        field_type_map[field_name] = field_type_str
    return field_type_map


def get_ondisk_type_map(clazz) -> dict:
    obj_type_map = get_object_type_map(clazz)
    field_type_map = {}
    for field, annotation in obj_type_map.items():
        if annotation not in SQL_TYPE_LOOKUP:
            raise Exception(f"SQL type mapping not found for {annotation}")
        field_type_map[field] = SQL_TYPE_LOOKUP[annotation]
    return field_type_map


async def get_ref_to_async_function(package, fn_name):
    for file in dir(package):
        if not file.startswith('__'):
            file_item_attr = getattr(package, file)
            if callable(file_item_attr) and file_item_attr.__name__ == fn_name:
                return file_item_attr


def get_package_classes(data_class_package, excluded_classes: list, base_object):
    excluded_classes += ["AbstractDataTable"]
    package_items = [getattr(data_class_package, name) for name in dir(data_class_package)
                     if not name.startswith('__')
                     and inspect.isclass(getattr(data_class_package, name))
                     and issubclass(getattr(data_class_package, name), base_object)
                     and name not in excluded_classes]
    return package_items


# @red
async def shell_exec_get_output(cmd: str, cwd=None) -> tuple:
    proc = await asyncio.create_subprocess_shell(

        cmd,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

    return proc.returncode, stdout.decode(), stderr.decode()
