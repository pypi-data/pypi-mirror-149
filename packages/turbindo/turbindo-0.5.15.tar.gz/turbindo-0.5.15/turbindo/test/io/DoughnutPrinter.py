from turbindo.runtime.instrumented_object import InstrumentedIO


class DoughnutPrinter(InstrumentedIO):
    async def move_arm(self, posx: int, posy: int) -> bool:
        return posx <= 8 and posy <= 8

    async def extrude_dough(self, units) -> bool:
        return units < 3

    async def get_dough_level(self) -> int:
        return 3

    async def get_filling_level(self) -> int:
        return 4
