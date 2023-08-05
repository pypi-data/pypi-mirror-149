from invoke import Config, Program

from .tasks import deploy


class BuildtoolsConfig(Config):
    prefix = 'rbx'


program = Program(config_class=BuildtoolsConfig, namespace=deploy.ns, version='2.20.1.dev273')
