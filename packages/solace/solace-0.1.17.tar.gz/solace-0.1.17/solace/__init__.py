from starlette.applications import Starlette
from starlette.types import ASGIApp
from .validator import SolaceValidator as SolaceValidator
from .config import Config
from .context import Context # this allows callers to do 'from solace import Context'
from .flow import SolaceFlow
from .importer import import_from_string
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

class Solace:
    """ creates an application instance """
    
    def __init__(self, **kwargs):
        
        self.debug = kwargs.get('debug', False)
        self.app_config_file = kwargs.get('app_config', "app.yaml")
        self.app_config = Config(self.app_config_file).__call__()
        self.plugins = []
        self.app = Starlette(
            debug = self.debug
        )

        if self.app_config.get('plugins', None) is not None:
            for plugin in self.app_config.get('plugins'):
                self.plugins.append(import_from_string(plugin))

        for route_config in self.app_config.get('routes'):
            ctx = Context(self.app_config)
            flow = SolaceFlow(ctx)
            
            for f in route_config.get('flow'):
                handler = import_from_string(f)
                if handler is None:
                    raise Exception(f"handler '{handler}' was unable to be imported")
                flow.stack.append(handler)

            route = Route(
                path = route_config.get('path'),
                endpoint = flow,
                methods = route_config.get('methods')
            )

            self.app.routes.append(route)

    def __call__(self) -> ASGIApp:
        """ returns a configured ASGIApp instance """
        if self.app_config.get('static_assets_dir') is not None:
            if self.app_config.get('static_assets_url') is not None:
                self.app.routes.append(
                    Mount(
                        self.app_config.get('static_assets_url'), 
                        app = StaticFiles(
                            directory = self.app_config.get('static_assets_dir')
                        ),
                        name="static"
                    )
                )
        return self.app
