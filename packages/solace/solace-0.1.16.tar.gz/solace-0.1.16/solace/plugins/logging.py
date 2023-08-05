""" A Logging Plugin for Solace (powered by Loguru) """

from solace.context import Context
from loguru import logger
import sys

async def logging(ctx: Context):
    """ provides logging support via Loguru to the Context object """
    ctx.trace("start of logging plugin")
    handler = {
        "sink": ctx.config.get('log_sink', sys.stderr),
        "level": ctx.config.get('log_level', "INFO").upper()
    }
    if ctx.config.get('log_format', None):
        handler["format"] = ctx.config.get('LOG_FORMAT')
    if ctx.config.get('log_type', 'text') == 'json':
        handler["serialize"] = True
    logger.configure(handlers = [handler])
    ctx.logger = logger
    ctx.trace("end of logging plugin")
    return ctx
