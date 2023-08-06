from starlette.types import *
from starlette.responses import *
from .templating import Jinja2Templates, _TemplateResponse
from starlette.exceptions import HTTPException
from inspect import getframeinfo, stack
from .config import Config

class ContextualHTTPException(HTTPException):
    line_number: int = None
    file_name: str = None
    function: str = None
    def __init__(self, status_code: int, detail: str = None, headers: dict = None) -> None:
        super().__init__(status_code, detail, headers)

class Context:
    
    def __init__(self, config: Config):
        self.config: Config = config
        self.frames: list = []
        self.headers: dict = {}
        self.code: int = 200

    @property
    def url(self) -> str:
        return self.request.url
    
    @property
    def method(self) -> str:
        return self.request.method
    
    @property
    def params(self) -> dict:
        return self.request.path_params
    
    @property
    def args(self) -> dict:
        return dict(self.request.query_params)
    
    def error(self, message: str, code: int = 400):
        """ interrupt the flow, and return a proper http error """
        caller = getframeinfo(stack()[1][0])
        e = ContextualHTTPException(
            status_code = code,
            detail = message,
            headers = self.headers
        )
        e.file_name = caller.filename
        e.function = caller.function
        e.line_number = caller.lineno
        if hasattr(self, 'logger'):
            self.logger.error(message)
            self.logger.debug(f"File Name: {caller.filename}")
            self.logger.debug(f"Line Number: {caller.lineno}")
            self.logger.debug(f"Function: {caller.function}")
        raise e
    
    def warn(self, message: str):
        """ display a warning message if a logger is configured """
        caller = getframeinfo(stack()[1][0])
        if hasattr(self, 'logger'):
            self.logger.warning(message)
            self.logger.debug(f"File Name: {caller.filename}")
            self.logger.debug(f"Line Number: {caller.lineno}")
            self.logger.debug(f"Function: {caller.function}")
    
    def info(self, message: str):
        """ display a info message if a logger is configured """
        caller = getframeinfo(stack()[1][0])
        if hasattr(self, 'logger'):
            self.logger.info(message)
            self.logger.debug(f"File Name: {caller.filename}")
            self.logger.debug(f"Line Number: {caller.lineno}")
            self.logger.debug(f"Function: {caller.function}")
    
    def trace(self, label: str = None):
        """ trace the context """
        if self.config.get('context_tracers_enabled') == True:
            caller = getframeinfo(stack()[1][0])
            frame = caller._asdict()
            if label:
                frame["label"] = label
            self.frames.append(frame)
    
    def text(self,
        content: typing.Any = None,
    ) -> PlainTextResponse:
        """ a plain text response """
        return PlainTextResponse(
            content = content,
            status_code = self.code,
            headers = self.headers
        )

    def json(self,
        content: typing.Any = None,
    ) -> JSONResponse:
        """ a json response """
        return JSONResponse(
            content = content,
            status_code = self.code,
            headers = self.headers
        )

    def html(self,
        content: typing.Any = None,
    ) -> HTMLResponse:
        """ an html response """
        return HTMLResponse(
            content = content,
            status_code = self.code,
            headers = self.headers
        )

    def view(self,
        template: str,
        data: dict = {}
    ) -> _TemplateResponse:
        """ a template based response """
        templates = Jinja2Templates(self.config.get('templates_dir'))
        return templates.TemplateResponse(
            name = template,
            context = data,
            status_code = self.code,
            headers = self.headers,
        )

    def file(self,
        path: str,
        file_name: str = None,
    ) -> FileResponse:
        """ a file response """
        return FileResponse(
            path = path,
            status_code = self.code,
            headers = self.headers
        )

    def stream(self,
        content: typing.Any = None,    
    ) -> StreamingResponse:
        """ a streaming based response """
        return StreamingResponse(
            content = content,
            status_code = self.code,
            headers = self.headers            
        )
