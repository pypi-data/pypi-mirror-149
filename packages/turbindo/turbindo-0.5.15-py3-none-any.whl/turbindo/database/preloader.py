from traceback import print_exc

from turbindo.log.logger import Logger
from turbindo.runtime.scheduler import OneShotTask, TaskContext
import yaml


class Preloader(OneShotTask):

    def __init__(self, yaml_file: str, db, ctx: TaskContext = TaskContext()):
        super().__init__(ctx)
        self.yaml_file = yaml_file
        self.db = db

    async def run(self):
        file_data = open(self.yaml_file).read()
        try:
            preload_struct: dict = yaml.safe_load(file_data)
        except Exception as e:
            Logger(self.__class__.__name__).error(e)
        for data_class, entries in preload_struct.items():
            try:
                writer = getattr(self.db, f"write{data_class}")
            except Exception as e:
                Logger(self.__class__.__name__).error(e)
            for key, vals in entries.items():
                try:
                    await writer(key, **vals)
                except Exception as e:
                    print_exc()
                    Logger(self.__class__.__name__).error(e)
