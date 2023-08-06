import argparse
import asyncio
import importlib
import sys
from typing import Dict

from turbindo.database.codegen import generate_data_accessors
from turbindo.log.logger import Logger


def main():
    parser = argparse.ArgumentParser()

    _context = "CLI"
    logger = Logger('main')

    parser.add_argument("--tests", help="run the testsuite", action="store_true", default=False)
    parser.add_argument("--test_suite", help="specify test suite", type=str, default="*")
    parser.add_argument("--test_case", help="specify test case from suite", type=str, default="*")
    parser.add_argument("--integration_tests", help="run integration tests", action="store_true", default=False)
    parser.add_argument("--io_recording", help="run integration tests", type=str, default="*")
    parser.add_argument("--io_mocking", help="run integration tests", type=str, default="*")
    parser.add_argument("--gen_accessors", help="generate the database accessor code", action="store_true",
                        default=False)
    parser.add_argument("--gen_test_accessors", help="generate the database accessor code", action="store_true",
                        default=False)
    parser.add_argument("--data_package", help="generate the database accessor code", type=str,
                        default="turbindo.database.default.data_objects")

    args = parser.parse_args()

    if args.tests or args.integration_tests:
        app_loop = asyncio.new_event_loop()

        from turbindo.test import test_system as test_system
        results: Dict[str, Exception] = app_loop.run_until_complete(
            test_system.run_tests(f"turbindo.test.suites{'.integration' if args.integration_tests else ''}",
                                  suite_name=args.test_suite,
                                  case_name=args.test_case))
        status = 0
        for n, e in results.items():
            if e is None:
                logger.log(f"{n}: Pass")
            else:
                status = 1
                logger.error(f"{n}: Fail")
                logger.error(f"{e}")
        from turbindo.database.impl import sqlite
        app_loop.run_until_complete(sqlite.Sqlite.conn.close())
        app_loop.stop()
        app_loop.close()
        import os
        os._exit(status)

    elif args.gen_accessors:
        app_loop = asyncio.new_event_loop()
        from turbindo.database.default import classes
        results = app_loop.run_until_complete(generate_data_accessors(classes))
        f = open("turbindo/database/default/accessors.py", "w").write(results)

    elif args.gen_test_accessors:
        app_loop = asyncio.new_event_loop()
        from turbindo.test.data import classes
        results = app_loop.run_until_complete(generate_data_accessors(classes))
        f = open("turbindo/test/data/accessors.py", "w").write(results)


if __name__ == '__main__':
    main()
