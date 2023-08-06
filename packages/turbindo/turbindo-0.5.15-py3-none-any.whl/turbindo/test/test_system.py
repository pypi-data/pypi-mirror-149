import datetime
import importlib
import inspect
import os
import traceback
import uuid
from os import listdir
from pathlib import Path
from typing import Type, Callable, Optional, Dict
from turbindo.test.base_test import BaseTest


async def inner_run_test_case(case, suite):
    turbindo_context = str(case)
    if "pre_test_setup" in dir(suite):
        pts = getattr(suite, "pre_test_setup")
        await pts()
    result: bool = await case()
    if "post_test_teardown" in dir(suite):
        ptt = getattr(suite, "post_test_teardown")
        await ptt()
    return result


async def run_test_case(case, suite, ex_capture=True) -> Optional[str]:
    if ex_capture:
        try:
            result: bool = await inner_run_test_case(case, suite)
            if not result:
                if "EXPECTED_FAIL" in dir(suite):
                    if case.__name__ in getattr(suite, "EXPECTED_FAIL"):
                        return None  # success, planned failure
                return f"test case {case.__name__} in suite {suite.__class__.__name__} returned false"
        except Exception as e:
            if "EXPECTED_FAIL" in dir(suite):
                if case.__name__ in getattr(suite, "EXPECTED_FAIL"):
                    return None  # success, planned failure
                else:
                    raise e
            else:
                raise e
    else:
        result: bool = await inner_run_test_case(case, suite)
        if not result:
            return f"got False return for {case.__name__}"

    return None


async def run_test_suite(suite) -> Dict[str, Optional[str]]:
    results: Dict[str, Optional[str]] = {}
    d_res = dir(suite)

    case_names = [case_name for case_name in d_res if
                  inspect.iscoroutinefunction(getattr(suite, case_name)) and case_name.startswith("test_")]
    suite_obj = suite()
    if "async_init" in dir(suite_obj):
        await suite_obj.async_init()
    for case_name in case_names:
        results[f"{suite.__qualname__}:{case_name}"] = await run_test_case(getattr(suite_obj, case_name), suite_obj)
    if "cleanup_tests" in dir(suite_obj):
        await suite_obj.cleanup_tests()
    return results


async def get_suites_in_test_package(package):
    package_base_path = Path(package.__file__).parent.absolute()
    package_files = [p for p in listdir(package_base_path) if p.endswith('.py')]
    package_contents = [os.path.basename(f).split('.')[0] for f in package_files if not f.startswith('_')]
    suites = []
    for file in package_contents:
        module = importlib.import_module(f"{package.__name__}.{file}")
        module_contents = dir(module)
        class_names = [attr_name for attr_name in module_contents if inspect.isclass(getattr(module, attr_name))]
        suite_names = [suite_name for suite_name in class_names if
                       issubclass(getattr(module, suite_name), BaseTest) and suite_name != "BaseTest"]
        suites += [getattr(module, suite_name) for suite_name in suite_names]
    return suites

async def run_test_package(package) -> Dict[str, Optional[str]]:
    results: Dict[str, Optional[str]] = {}
    for suite in await get_suites_in_test_package(package):
        s_res: Dict[str, Optional[str]] = await run_test_suite(suite)
        results.update(s_res)
    return results




async def get_case(suite: Type, case_name) -> Callable:
    s_obj = suite()
    suite_contents = dir(s_obj)
    if case_name not in suite_contents:
        raise Exception(f"no such test case {case_name} in suite {s_obj.__qualname__}")
    case = getattr(s_obj, case_name)
    assert inspect.iscoroutinefunction(case)
    return case


async def get_suite(package, suite_name) -> Type:
    module = importlib.import_module(f"{package.__name__}.{suite_name}")
    package_contents = dir(module)
    if suite_name not in package_contents:
        raise Exception(f"no such test suite {suite_name} in package {package.__name__}")
    suite = getattr(module, suite_name)
    assert issubclass(suite, BaseTest)
    return suite


async def run_tests(package_name,
                    suite_name='*',
                    case_name='*',
                    result_writer=None,
                    ex_capture=True) -> Dict[str, Optional[str]]:

    package = importlib.import_module(package_name)
    if case_name != "*":
        assert suite_name != "*"
        suite = await get_suite(package, suite_name)
        case = await get_case(suite, case_name)
        if ex_capture:
            try:
                suite_obj = suite()
                await run_test_case(case, suite_obj)
            except Exception as e:
                traceback.print_exc()
                return {case_name: e}
        else:
            suite_obj = suite()
            results = await run_test_case(case, suite_obj)
            return {case_name: results}
        return {case_name: None}

    if suite_name != "*":
        module = importlib.import_module(f"{package.__name__}.{suite_name}")
        suite = getattr(module, suite_name)
        results = await run_test_suite(suite)
        return results
    results = await run_test_package(package)

    if result_writer is not None:
        time = datetime.datetime.now()
        run_id = uuid.uuid4()
        await result_writer(results, time, str(run_id))

    return results
