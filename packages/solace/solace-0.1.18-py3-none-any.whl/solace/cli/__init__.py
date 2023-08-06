import os
import sys
import typer
import uvicorn
import yaml

from typing import Optional

cli = typer.Typer()

app_py = """from solace import Solace

app = Solace()

"""

main_py = """from solace import Context

async def hello(ctx: Context):
    return ctx.text("Hello, World!")

"""

dockerfile_tpl = """FROM python:slim-bullseye

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src /app/src/
COPY static /app/static/
COPY templates /app/templates
COPY app.yaml /app/app.yaml

CMD ["uvicorn", "src.__solace__:app", "--host", "0.0.0.0", "--port", "5000"]
"""

default_config = {
    "env_name": "solace_dev",
    "env_type": "dev",
    "log_level": "debug",
    "static_assets_dir": "static",
    "static_assets_url": "/static",
    "templates_dir": "templates",
    "http_exception_type": "text",
    "context_tracers_enabled": False,
    "enable_dynamic_routes": False,
    "dynamic_routes_secret": None,
    "routes": [
        {
            "path": "/",
            "methods": ["GET"],
            "flow": ["src.main:hello"]
        }
    ]
}


def write_app():
    os.mkdir("__solace__")
    os.chdir("__solace__")
    f = open("__init__.py", "w+")
    f.write(app_py)
    f.close()

def write_dockerfile():
    f = open("Dockerfile", "w+")
    f.write(dockerfile_tpl)
    f.close()

def write_config():

    with open("app.yaml", "w+") as fp:
        yaml.safe_dump(default_config, fp, sort_keys = False)

def write_src():
    os.mkdir('src')
    os.chdir('src')
    f = open('main.py', 'w+')
    f.write(main_py)
    f.close()

def write_req():
    f = open('requirements.txt', 'w+')
    f.write("solace")
    f.close()

@cli.command()
def init(
        name: str,
    ):
    # TODO: add a "prompt" style wizard similar to npm init (uses PyInquirer)
    """
    initialize a new Solace Project
    """
    # TODO: bring in solace.config object
    # and use that to create proper dir
    # structures
    try:
        os.mkdir(name)
        os.chdir(name)
        os.mkdir("static")
        os.mkdir("templates")
        write_config()
        write_dockerfile()
        write_src()
        write_app()
        write_req()

    except FileExistsError:
        typer.echo(f"ERROR: {name} already exists")
        sys.exit(1)

@cli.command()
def dev(
    app: str = typer.Option("src.__solace__:app"),
    host: Optional[str] = typer.Option("127.0.0.1"),
    port: Optional[int] = typer.Option(5000),
    log_level: Optional[str] = typer.Option("debug"), # this is because it's a "dev server"
    reload: Optional[bool] = typer.Option(True),
    debug: Optional[bool] = typer.Option(True) # this is because it's a "dev server"
    ):
    """
    start a local development server
    """
    sys.path.append(os.getcwd())
    uvicorn.run(
        app = app,
        host=host, 
        port=port, 
        log_level=log_level,
        reload=reload,
        reload_includes=["*.py", "*.toml", "*.json", "*.yaml", "*.env", ".env", "*.html", "*.js", "*.css"],
        debug=debug,
        factory = False
    )
