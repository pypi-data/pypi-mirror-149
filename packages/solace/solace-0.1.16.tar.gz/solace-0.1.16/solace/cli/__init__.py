import os
import sys
import typer
import uvicorn

from typing import Optional

cli = typer.Typer()

main_py = """from solace import Solace

async def handler(ctx):
    ctx.body = "Hello, World!"
    return ctx

app = Solace()
app.get("/", handler)

"""

dot_env_tpl = """ENV_NAME = "dev1"
ENV_TYPE = "dev" # should be set to one of these: ["dev", "test", "stage", "prod"]
LOG_LEVEL = "debug"
# LOG_FORMAT = "" # https://loguru.readthedocs.io/en/stable/api/logger.html#record
# LOG_FILE = "solace.application.log"
# LOG_TYPE = "text"

# STATIC_ASSETS_DIR = "static"
# STATIC_ASSETS_URL = "/static"

# TEMPLATES_DIR = "templates"

"""

dockerfile_tpl = """
"""

def write_dockerfile():
    f = open("Dockerfile", "w+")
    f.write(dockerfile_tpl)
    f.close()

def write_env():
    f = open(".env", "w+")
    f.write(dot_env_tpl)
    f.close()

def write_src():
    os.mkdir('src')
    os.chdir('src')
    f = open('main.py', 'w+')
    f.write(main_py)
    f.close()

@cli.command()
def init(
        name: str,
        templating: Optional[bool] = typer.Option(True),
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
        # if templating:
        #     if STATIC_ASSETS_DIR is not None:
        #         os.mkdir(STATIC_ASSETS_DIR)
        #     if TEMPLATES_DIR is not None:
        #         os.mkdir(TEMPLATES_DIR)
        write_env()
        write_dockerfile()
        write_src()

    except FileExistsError:
        typer.echo(f"ERROR: {name} already exists")
        sys.exit(1)

@cli.command()
def dev(
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
        "src.main:app", 
        host=host, 
        port=port, 
        log_level=log_level,
        reload=reload,
        reload_includes=["*.py", "*.toml", "*.json", "*.yaml", "*.env", ".env", "*.html", "*.js", "*.css"],
        debug=debug,
        factory = False
    )
