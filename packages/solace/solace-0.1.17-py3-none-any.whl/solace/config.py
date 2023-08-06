import yaml
import os
import json

from typing import Any, IO

class Loader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)


def _include(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""

    filename = os.path.abspath(os.path.join(loader._root, loader.construct_scalar(node)))
    extension = os.path.splitext(filename)[1].lstrip('.')

    with open(filename, 'r') as f:
        if extension in ('yaml', 'yml'):
            return yaml.load(f, Loader)
        elif extension in ('json', ):
            return json.load(f)
        else:
            return ''.join(f.readlines())

def _env(loader: Loader, node: yaml.Node) -> Any:
    """set value of key at node from environment variable"""
    if node.value in os.environ:
        return os.environ.get(node.value)
    raise Exception('undefined environment variable referenced %s' % (node.value))

yaml.add_constructor('!include', _include, Loader)
yaml.add_constructor('!env', _env, Loader)

# NOTE: this would add support for fetching config values using a HTTP GET request
# yaml.add_constructor('!http', _env, Loader)

class Config:
 
    def __init__(self, config = "config.yaml"):
        """ 
        The constructor for Config class.
        """
        self.props = {}
        with open(config, 'r') as f:
            conf = yaml.load(f, Loader=Loader)
            if conf is not None:
                self.props = conf

    def __call__(self) -> dict:
        return self.props
