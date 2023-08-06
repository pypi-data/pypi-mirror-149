import inspect
import logging
import os
import pathlib
from datetime import datetime


def find_local_on_stack(var_name, frame):
    while True:
        if var_name in frame.f_locals:
            return frame.f_locals[var_name]
        else:
            if frame.f_back is not None:
                frame = frame.f_back
            else:
                return None


class Logger:
    default_log_level = logging.DEBUG

    def __init__(self, name, out_file=None):
        logging.basicConfig()
        self.trace_enabled = False
        self.logger = logging.getLogger(name)
        self.logger.setLevel(Logger.default_log_level)
        self.name = name
        self.out_file = out_file
        if "TURBINDO_LOG_FILE" in os.environ:
            self.out_file = open(os.environ["TURBINDO_LOG_FILE"], "a")
        if out_file is not None:
            if "TURBINDO_LOG_FILE_OVERRIDE" not in os.environ:
                self.out_file = open(out_file, "a")

        ch = logging.StreamHandler()
        ch.setLevel(Logger.default_log_level)

    def set_level(self, level):
        self.logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)

    def set_trace(self, switch: bool):
        self.trace_enabled = switch

    def log(self, message):
        self.logger.info(self.process(message))

    def debug(self, message):
        self.logger.debug(self.process(message))

    def info(self, message):
        self.logger.info(self.process(message))

    def error(self, message):
        self.logger.error(self.process(message))

    def trace(self, message):
        if self.trace_enabled:
            self.logger.debug(self.process(message))

    def process(self, message) -> str:
        def find_caller(frame):
            filename, line_number, function_name, lines, index = inspect.getframeinfo(frame)
            if 'turbindo/log/logger.py' in filename:
                return find_caller(frame.f_back)
            return filename, line_number

        filename, line_number = find_caller(inspect.currentframe())

        turbindo_home = pathlib.Path(__file__).parent.parent.parent.resolve().__str__()
        wd = os.getcwd()
        if "site-packages" in filename:
            idx = filename.split('/').index("site-packages")
            remainder = filename.split('/')[idx + 1:]
            nfn = "/".join(remainder)
        elif wd in turbindo_home:
            nfn = filename.replace(turbindo_home, "").lstrip("/")
        else:
            nfn = filename.replace(wd, "").lstrip("/")
        log_line = f'[{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}]' \
                   f' {nfn}:{line_number}' \
                   f'[{find_local_on_stack("turbindo_context", inspect.currentframe()) or ""}]' \
                   f' "{message}"'
        if self.out_file is not None:
            self.out_file.write(log_line)
        return log_line
