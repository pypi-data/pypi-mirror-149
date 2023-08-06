import aiodocker

from turbindo.log.logger import Logger
from turbindo.runtime.instrumented_object import InstrumentedIO


class AIODocker(InstrumentedIO):
    def __init__(self):
        self.aiodocker = aiodocker.Docker()
        self.logger = Logger(self.__class__.__name__)

    async def exec_ctr_cmd(self, ctr_id, cmd):
        ctr = await self.aiodocker.containers.get(ctr_id)
        await ctr.exec(cmd)

    async def get_arch(self, image) -> str:
        pass

    async def assert_arch(self, image, arch):
        assert arch == await self.get_arch(image)

    async def tag_image(self, img, repo, tag):
        await self.aiodocker.images.tag(img, repo, tag=tag)
