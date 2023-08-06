import jinja2
import yaml
from box import Box
import os


class TurbindoConfiguration():
    def __init__(self, path='./', file='config.yaml'):
        yaml.SafeLoader.yaml_implicit_resolvers = {
            k: [r for r in v if r[0] != 'tag:yaml.org,2002:timestamp'] for
            k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
        }
        templateLoader = jinja2.FileSystemLoader(searchpath=path)
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(file)
        config_yaml_str = template.render(ENV=os.environ)
        self.data = yaml.safe_load(config_yaml_str)
        self.config = Box(self.data)
