from typing import Callable
from starlette.applications import Starlette
from starlette.types import ASGIApp
from .flow import SolaceFlow
from .validator import SolaceValidator as SolaceValidator
from .context import Context
from .config import Config
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

class Solace:
    """ creates an application instance """
    
    def __init__(self, **kwargs):
        
        self.debug = kwargs.get('debug', False)
        self.config_file = kwargs.get('config_file', "config.yaml")
        self.config = Config(self.config_file)
        self.handlers = []

        self.app = Starlette(
            debug = self.debug
        )

    def use(self, *handlers: Callable):
        for h in handlers:
            self.handlers.append(h)
    
    def _populate(self, path: str, method: str, *handlers:callable):
        
        ctx = Context(self.config)

        flow = SolaceFlow(ctx)
        self.handlers.extend(handlers)
        for h in self.handlers:
            flow.stack.append(h)
        self.app.add_route(
            path = path, 
            route = flow,
            methods = [method]
        )

    def get(self, path: str, *handlers: Callable):
        """ adds a GET request flow handler """
        self._populate(path, 'GET', *handlers)
    
    def head(self, path: str, *handlers: Callable):
        """ adds a HEAD request flow handler """
        self._populate(path, 'HEAD', *handlers)
    
    def post(self, path: str, *handlers: Callable):
        """ adds a POST request flow handler """
        self._populate(path, 'POST', *handlers)
    
    def put(self, path: str, *handlers: Callable):
        """ adds a PUT request flow handler """
        self._populate(path, 'PUT', *handlers)
    
    def delete(self, path: str, *handlers: Callable):
        """ adds a DELETE request flow handler """
        self._populate(path, 'DELETE', *handlers)
    
    def connect(self, path: str, *handlers: Callable):
        """ adds a CONNECT request flow handler """
        self._populate(path, 'CONNECT', *handlers)
    
    def options(self, path: str, *handlers: Callable):
        """ adds a OPTIONS request flow handler """
        self._populate(path, 'OPTIONS', *handlers)
    
    def trace(self, path: str, *handlers: Callable):
        """ adds a TRACE request flow handler """
        self._populate(path, 'TRACE', *handlers)
    
    def patch(self, path: str, *handlers: Callable):
        """ adds a PATCH request flow handler """
        self._populate(path, 'PATCH', *handlers)
    
    def ws(self, path: str, *handlers: Callable):
        flow = SolaceFlow()
        self.handlers.extend(handlers)
        for h in self.handlers:
            flow.stack.append(h)
        self.app.add_websocket_route(
            path = path, 
            route = flow,
        )

    def __call__(self) -> ASGIApp:
        """ returns a configured ASGIApp instance """
        if self.config.get('static_assets_dir') is not None:
            if self.config.get('static_assets_url') is not None:
                self.app.routes.append(
                    Mount(
                        self.config.get('static_assets_url'), 
                        app = StaticFiles(
                            directory = self.config.get('static_assets_dir')
                        ),
                        name="static"
                    )
                )
        return self.app
