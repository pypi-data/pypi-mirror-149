""" A Simple SQL plugin for Solace powered by Encode's Databases Project """
from solace.context import Context
from databases import Database
from pymysql.err import OperationalError

async def sqlite_provider(ctx: Context):
    ctx.trace("start of sqlite_provider plugin")
    dbname = ctx.config.get('SQLITE_DB_NAME', 'default.db')
    database = Database(f'sqlite+aiosqlite:///{dbname}')
    await database.connect()
    if database.is_connected:
        ctx.db = database
    else:
        ctx.error("failed to connect to sqlite database")
    ctx.trace("end of sqlite_provider plugin")
    return ctx

async def mysql_provider(ctx: Context):
    ctx.trace("start of mysql_provider plugin")
    try:
        db_name = ctx.config.get('MYSQL_DB_NAME', 'default')
        db_host = ctx.config.get('MYSQL_DB_HOST', '127.0.0.1')
        db_port = ctx.config.get('MYSQL_DB_PORT', 3306)
        db_user = ctx.config.get('MYSQL_DB_USER', None)
        db_pass = ctx.config.get('MYSQL_DB_PASS', None)
        database = Database(f'mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')
        await database.connect()
    except OperationalError as e:
        ctx.error(str(e))

    if database.is_connected:
        ctx.db = database
    else:
        ctx.error("failed to connect to mysql/mariadb database")
    
    ctx.trace("end of mysql_provider plugin")
    return ctx
