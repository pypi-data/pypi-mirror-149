import io
import yaml
from starlette.applications import Starlette
from starlette.types import ASGIApp
from .validator import SolaceValidator as SolaceValidator
from .config import Config
from .context import Context # this allows callers to do 'from solace import Context'
from .flow import SolaceFlow
from .importer import import_from_string
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from box import Box

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
            ctx.store = Box({})
            flow_name = route_config.get('name', None)
            flow = SolaceFlow(ctx, flow_name)
            for f in route_config.get('flow'):
                flow.functions.append(f)
                handler = import_from_string(f)
                if handler is None:
                    raise Exception(f"handler '{handler}' was unable to be imported")
                flow.stack.append(handler)

            route = Route(
                path = route_config.get('path'),
                endpoint = flow,
                methods = route_config.get('methods'),
                name = flow_name
            )

            self.app.routes.append(route)
        
        if self.app_config.get('enable_dynamic_routes') == True:
            # TODO: check if dynamic_route_secret is set
            # and validate secret is correct
            route = Route(
                path = "/_solace/routes",
                endpoint = self.dynamic_routes_handler,
                methods = ["GET", "POST", "DELETE"]
            )
            self.app.routes.append(route)
    
    async def dynamic_routes_handler(self, req: Request):
        """ The Dynamic Routes Handler """
        if req.method == "GET":
            routes = []
            for route in self.app.routes:
                if type(route) is not Mount:
                    if hasattr(route.endpoint, 'functions'):
                        r = {
                            "name": route.endpoint.name,
                            "path": route.path,
                            "flow": route.endpoint.functions,
                            "methods": list(route.methods)
                        }
                        routes.append(r)
            format = req.query_params.get("format", "json")
            if format == "yaml":
                out = io.StringIO()
                yaml.safe_dump(routes, out, sort_keys = False)
                return PlainTextResponse(out.getvalue())
            else:
                return JSONResponse(routes)

        
        if req.method == "DELETE":
            route_name = req.query_params.get("name", None)
            if route_name is not None:
                for route in self.app.routes:
                    if route.name == route_name:
                        self.app.routes.remove(route)
                        return JSONResponse({ "status": "OK" })
            return JSONResponse({ "status": "NOT OK" }, status_code = 400)
        
        if req.method == "POST":

            route_data = await req.json()
            # TODO: validate request data
            
            for route in self.app.routes:
                if route_data.get('name') is not None:
                    if route.name == route_data.get('name'):
                        self.app.routes.remove(route)

            ctx = Context(self.app_config)
            flow_name = route_data.get('name', None)
            flow = SolaceFlow(ctx, flow_name)
            for f in route_data.get('flow'):
                flow.functions.append(f)
                handler = import_from_string(f)
                if handler is None:
                    raise Exception(f"handler '{handler}' was unable to be imported")
                flow.stack.append(handler)

            self.app.routes.append(
                Route(
                    path = route_data.get('path'),
                    name = route_data.get('name'),
                    methods = route_data.get('methods'),
                    endpoint = flow
                )
            )
            
            return JSONResponse({ "status": "OK" }, status_code = 201)

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
