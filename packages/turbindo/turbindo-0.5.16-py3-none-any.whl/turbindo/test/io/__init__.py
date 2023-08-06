from turbindo.runtime.io_context import IOContext
from turbindo.test.io.DoughnutPrinter import DoughnutPrinter
from turbindo.input_output.crypto import CryptographyManager

def type_or_string(input):
    if issubclass(str, input):
        return input
    return input.__name__


async def setup(recording=(), mocking=()):
    recording = tuple([type_or_string(r) for r in recording])
    mocking = tuple([type_or_string(m) for m in mocking])


    await IOContext.register(DoughnutPrinter,
                             recording="DoughnutPrinter" in recording,
                             mocking="DoughnutPrinter" in mocking)
    await IOContext.register(CryptographyManager,
                             recording="CryptographyManager" in recording,
                             mocking="CryptographyManager" in mocking)


def dough() -> DoughnutPrinter:
    return IOContext.lookup(DoughnutPrinter)


def crypto() -> CryptographyManager:
    return IOContext.lookup(CryptographyManager)
