""" A Redis Plugin for Solace """
import redis

async def redis_plugin(ctx):
    """ A simple redis plugin provider """
    # TODO: add authentication support 
    # TODO: look into async redis support
    ctx.trace("start of redis plugin")
    host = ctx.config.get('REDIS_HOST', 'localhost')
    port = ctx.config.get('REDIS_PORT', 6379)
    db = ctx.config.get('REDIS_DB', 0)
    password = ctx.config.get('REDIS_PASSWORD', None)
    socket_timeout = ctx.config.get('REDIS_SOCKET_TIMEOUT', None)

    r = redis.Redis(
        host = host,
        port = port,
        db = db,
        password = password,
        charset='utf-8', 
        errors='strict',
        socket_timeout = socket_timeout
    )
    
    if not ctx.config.get('REDIS_DISABLE_PING_ON_CONNECT', None):
        try:
            r.ping()
        except Exception as e:
            ctx.error("redis ping failed")

    ctx.redis = r
    ctx.trace("end of redis plugin")
    return ctx
