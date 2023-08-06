""" 
SolaceFlow is an ASGI Application that provides
the ability to create composable "flows" that
share a common context object. Solace is heavily
inspired by the Koa.js framework, found here
https://koajs.com/

The reason for creating this is to enable what
I like to think of as "truly reusable code"
so that a developer can create flows made up of
generic functions and then compose those flows
into their applications to suit their needs.
"""

from .context import Context, ContextualHTTPException
import sys
import copy
from starlette.types import Scope, Send, Receive, ASGIApp
from boltons.tbutils import ExceptionInfo
from starlette.routing import iscoroutinefunction_or_partial
from starlette.requests import *
from starlette.responses import *
from .templating import _TemplateResponse


VALID_RESPONSE_TYPES = (
    Response, 
    JSONResponse, 
    StreamingResponse, 
    PlainTextResponse,
    _TemplateResponse,
    HTMLResponse,
    RedirectResponse,
    FileResponse
)

class SolaceFlow:
    """ Creates a SolaceFlow application instance. """

    def __init__(self, ctx: Context):
        self.stack = []
        self.ctx = ctx

    async def _stack(self, ctx: Context) -> ASGIApp:
        try:
            for handler in self.stack:
                if iscoroutinefunction_or_partial(handler):
                    rv = await handler(ctx)
                else:
                    rv = handler(ctx)
                
                # # we have a return value...
                if rv is not None:
                    # NOTE: if we have a context object,
                    # then we need to update it before
                    # going into the next flow handler.
                    if isinstance(rv, Context):
                        ctx = rv
                    
                    # if the return value is a valid Response type,
                    # then we will immediately return, stopping any
                    # futher handlers in the flow from executing.
                    elif issubclass(type(rv), VALID_RESPONSE_TYPES):
                        return rv

        except ContextualHTTPException as e:
            exception_info = ExceptionInfo.from_exc_info(*sys.exc_info())
            error_message = "Internal Server Error\n"
            self.ctx.code = 500
            if self.ctx.config.get('http_exception_type') == "json":
                error = {"message": "Internal Server Error"}
                if self.ctx.config.get('env_type') == "dev":
                    error["error"] = e.detail
                    error["file_name"] = e.file_name
                    error["line_number"] = e.line_number
                    error["function"] = e.function
                    error["exception"] = exception_info.to_dict()
                    if self.ctx.config.get('context_tracers_enabled') == True:
                        error["solace_trace"] = ctx.frames
                
                return self.ctx.json(error)
            else:
                if self.ctx.config.get('context_tracers_enabled') == True:
                    error_message += "Solace Trace:\n"
                    for frame in ctx.frames:
                        error_message += "-------------------------------------------------------------------------------\n"
                        error_message += "File Name: " + frame.get('filename') + "\n"
                        error_message += "Line Number: " + str(frame.get('lineno')) + "\n"
                        error_message += "Function: " + frame.get('function') + "\n"
                        if frame.get('label', None):
                            error_message += "Label: " + frame.get('label') + "\n"
                
                if self.ctx.config.get('env_type') == "dev":
                    error_message += "-------------------------------------------------------------------------------\n"
                    error_message += "Error: " + e.detail
                    error_message += "\n"
                    error_message += "-------------------------------------------------------------------------------\n"
                    error_message += "Error Context:\n"
                    error_message += "File Name: " + e.file_name + "\n"
                    error_message += "Line Number: " + str(e.line_number) + "\n"
                    error_message += "Function: " + e.function + "\n"
                    error_message += "-------------------------------------------------------------------------------\n"
                
                # TODO: support html version of this?
                return self.ctx.text(error_message)
        
        except Exception as e:
            exception_info = ExceptionInfo.from_exc_info(*sys.exc_info())
            self.ctx.code = 500
            error_message = "Internal Server Error\n"
            if self.ctx.config.get('env_type') == "dev":
                error_message += "-------------------------------------------------------------------------------\n"
                error_message += "Error: " + str(e)
                error_message += "\n"
                error_message += "-------------------------------------------------------------------------------\n"
                error_message += exception_info.get_formatted()
                error_message += "\n"
                error_message += "-------------------------------------------------------------------------------\n"

            return self.ctx.text(error_message)

        return ctx

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # NOTE: this creates a "deep copy" of the context object per flow
        # This is to prevent "context collisions" that can occur by
        # sharing a single context object across the application.
        # This is more efficient than instaniating a new object for each flow.
        ctx = copy.deepcopy(self.ctx)
        ctx.request = Request(
            scope = scope,
            receive = receive,
            send = send
        )
        app = await self._stack(ctx) # this should return an ASGIApp object
        await app(scope, receive, send)
