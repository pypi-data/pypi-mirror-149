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
        return os.environ[node.value]
    raise Exception('undefined environment variable referenced %s' % (node.value))

yaml.add_constructor('!include', _include, Loader)
yaml.add_constructor('!env', _env, Loader)

class Config:
 
    def __init__(self, config = "config.yaml"):
        """ 
        The constructor for Config class.
        """
        with open(config, 'r') as f:
            confopts = yaml.load(f, Loader=Loader)
            if confopts is not None:
                for opt in confopts:
                    setattr(self, opt, confopts[opt])

    def get(self, attr: str, default: Any = None):
        """ gets the value of the given attribute """
        if hasattr(self, attr):
            return getattr(self, attr)
        return default
    
    def set(self, attr: str, value: Any):
        """ sets the value of the given attribute """
        setattr(self, attr, value)
