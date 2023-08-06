import json
import sys

import docker as dc
import subprocess

from turbindo.runtime.instrumented_object import InstrumentedIO
from turbindo.log.logger import Logger

logger = Logger(__file__)


class Docker(InstrumentedIO):
    def __init__(self):
        self.docker = dc.from_env()
        self.logger = Logger('DockerTest')

    def create_ctr(self, base_image, cmd, name, volumes: list):
        res = self.docker.create_container(base_image, name=name, command=cmd, volumes=volumes)
        self.docker.exec_start(res['Id'])
        return res

    def tag_image(self, img, repo, tag):
        self.docker.images.get(img).tag(repository=repo, tag=tag)

    def build_image(self, dockerfile: str, buildpath: str, buildargs: dict, tag: str, extra: str = ""):
        bargstr = ""
        squash = ""  # "--squash=false "
        for k, v in buildargs.items():
            if type(v) is dict or type(v) is list:
                v = json.dumps(v, separators=(',', ':'))
            bargstr += f" --build-arg {k}='{v}'"
        buildstring = f"ls /{buildpath} && docker build {squash} {extra} -t {tag} {bargstr} -f {dockerfile} {buildpath}"
        self.logger.info(buildstring)
        stdout_value, stderr_value = None, None
        try:
            proc = subprocess.Popen(buildstring,
                                    shell=True,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            stdout_value, stderr_value = proc.communicate()

        except subprocess.CalledProcessError as e:
            print('err exit code: {}'.format(e.returncode))
            print('err stdout: {}'.format(e.output.decode(sys.getfilesystemencoding())))
            print('err stderr: {}'.format(e.stderr.decode(sys.getfilesystemencoding())))

        self.logger.info(f'stdout:{stdout_value.decode("unicode_escape")}')
        self.logger.info(f'stderr:{stderr_value.decode()}')
        if "layer does not exist" in stderr_value.decode():
            self.build_image(dockerfile, buildpath, buildargs, tag, extra)
        self.logger.debug(f'docker build return code {proc.returncode}')
        # assert proc.returncode == 0

        # self.docker.build(buildpath, tag=tag, buildargs=buildargs)

    def get(self, name):
        l = self.docker.containers.list(all=True)
        filter = [c for c in l if c.name == name]
        return filter[0]

    def exists(self, name) -> bool:
        l = self.docker.containers.list(all=True)
        filter = [c for c in l if c.name == name]
        return filter != []

    def is_running(self, name) -> bool:
        l = self.docker.containers.list()
        filter = [c for c in l if c.name == name]
        return filter != []

    def run(self, *args, **kwargs):
        ret = self.docker.containers.run(*args, **kwargs)
        return ret

    def exec_ctr_cmd(self, ctr, cmd):
        containter = self.docker.containers.get(ctr)
        containter.exec_run()

    def inspect(self, ctr):
        return self.docker.api.inspect_container(ctr)

    def kill(self, id):
        return self.docker.api.kill(resource_id=id)

    def remove(self, id):
        return self.docker.api.remove_container(resource_id=id)
