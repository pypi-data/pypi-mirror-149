from __future__ import annotations
import subprocess
from turbindo.runtime.instrumented_object import InstrumentedIO
from turbindo.configuration import TurbindoConfiguration

from turbindo.log.logger import Logger


class Shell(InstrumentedIO):
    def __init__(self):
        self.logger = Logger("ShellClient")
        self.config = TurbindoConfiguration().config

    def run_cmd(self, cmdstring: list | str, stdin=None) -> tuple:
        if isinstance(cmdstring, str):
            cmdstring=cmdstring.split(' ')
        self.logger.debug(f"will run {cmdstring}")
        res = subprocess.run(cmdstring, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.logger.debug(f"return: code: {res.returncode} out: {res.stdout} err: {res.stderr}")
        return res.stdout, res.stderr, res.returncode
