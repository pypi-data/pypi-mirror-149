from __future__ import annotations

import functools
from typing import List

from box import Box
from transitions.extensions import AsyncMachine

from turbindo.database.base_object import Serialization
from turbindo.log.logger import Logger
from turbindo.runtime.exceptions import NoRowFoundException


class TurbindoMachine:
    def __init__(self, db_id: str,
                 inital_state: str,
                 state_list: List[str],
                 db_reader: callable,
                 db_writer: callable,
                 machine_class: type = AsyncMachine):
        self.suppress_db_init = False
        self.initalized = False
        self.inital_state = inital_state
        self.state_list = state_list
        self.data = Box()
        self.db_reader = functools.partial(db_reader, db_id)
        self.db_writer = functools.partial(db_writer, db_id)
        self.machine = machine_class(model=self,
                                    initial=inital_state,
                                    states=state_list,
                                    after_state_change=['write_db', 'read_db'],
                                    before_state_change=['check_transition'])

    def generate_state_diagram(self, output_path):
        self.machine.model.get_graph().draw(f'{output_path}', prog='dot')

    async def check_transition(self):
        Logger(self.__class__.__name__).debug(f"before_state_change {self.state}")
        assert self.initalized

    async def write_db(self):
        if not self.suppress_db_init:
            Logger(self.__class__.__name__).debug(f"after_state_change {self.state}")
            await self.db_writer(state=self.state)

    async def read_db(self):
        if not self.suppress_db_init:
            self.data = Box((await self.db_reader()).serialize(Serialization.DICT))

    async def abuild(self) -> TurbindoMachine:
        #@todo right way to suppress db i/o for diagram output
        if type(self.machine) is AsyncMachine and not self.suppress_db_init:
            try:
                self.data = await self.db_reader()
            except NoRowFoundException as e:
                await self.db_writer()
        self.initalized = True
        return self

    def declare_transition(self,
                           trigger_name: str,
                           from_state: str | List[str],
                           to_state: str,
                           before: str | callable | List[callable] | List[str],
                           after: str | callable | List[callable] | List[str],
                           conditions: str | list = None,
                           prepare: str | list = None
                           ) -> TurbindoMachine:
        if isinstance(before, list):
            before = [b.__name__ for b in before]
        elif callable(before):
            before = before.__name__
        elif isinstance(before, str):
            pass
        else:
            raise Exception("before is not {callable | List[callable]}")
        if isinstance(after, list):
            after = [a.__name__ for a in after if callable(after)]
        elif callable(after):
            after = after.__name__
        elif isinstance(after, str):
            pass
        else:
            raise Exception("after is not {callable | List[callable]}")

        self.machine.add_transition(trigger_name,
                                    from_state,
                                    to_state,
                                    before=before,
                                    after=after,
                                    conditions=conditions,
                                    prepare=prepare)

        return self
