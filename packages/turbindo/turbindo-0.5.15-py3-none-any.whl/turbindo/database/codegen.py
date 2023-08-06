import inspect
import os
from pathlib import Path

import jinja2

import turbindo.templates
from turbindo.database import AbstractDataTable
from turbindo.util import get_package_classes, get_object_type_map


async def generate_data_accessors(data_class_pkg):
    package_classes = get_package_classes(data_class_pkg, ["AbstractDataTable"], AbstractDataTable)
    path = os.path.abspath(Path(turbindo.templates.__file__).parent.absolute())
    template_loader = jinja2.FileSystemLoader(searchpath=path)
    template_enviorn = jinja2.Environment(loader=template_loader)

    class_prop_map = {}
    classtypes = {}
    class_type_map = {}

    for clazz in package_classes:
        classtypes[clazz.__name__] = get_object_type_map(clazz)
        members = [i[0] for i in inspect.getmembers(clazz, lambda o: isinstance(o, property))]
        members = [i for i in members if i != 'id']
        class_prop_map[clazz.__name__] = members
        print(class_prop_map)

    def doubleq(sl: list):
        return [f"{o}={o}" for o in sl]

    template_enviorn.filters['doubleq'] = doubleq
    data_accessors_template_file = "data_accessors.py.j2"
    template = template_enviorn.get_template(data_accessors_template_file)

    for clazz, data in classtypes.items():
        entries = []
        for k, v in data.items():
            if k != "id":
                entries.append(f"{k}:{v}")
        class_type_map[clazz] = entries

    accessor_python_code = template.render({
        "data_objects": package_classes,
        "class_type_map": class_type_map,
        "class_prop_map": class_prop_map,
        "data_class_pkg": data_class_pkg.__name__
    })

    return accessor_python_code
