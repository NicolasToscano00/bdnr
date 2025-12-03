# # Inicializa cliente Redis en modo cluster aware.
# # Implementa helper get_redis().

# import json
# import logging
# from app.config import settings
# import redis.asyncio as redis

# _logger = logging.getLogger(__name__)

# _redis = None

# async def get_redis():
#     """
#     Returns an async redis client. If you move to a real Redis Cluster,
#     modify this function to use redis.asyncio.cluster.RedisCluster and
#     pass startup_nodes.
#     """
#     global _redis
#     if _redis is None:
#         # Using from_url keeps it simple for single-node or sentinel-style URLs.
#         _redis = redis.from_url(settings.REDIS_URL, decode_responses=False)
#     return _redis

# # Helper that reads JSON using RedisJSON if available, otherwise fallback to GET/SET of JSON string
# async def json_get(key):
#     r = await get_redis()
#     try:
#         # Try RedisJSON module command
#         data = await r.execute_command("JSON.GET", key)
#         if data is None:
#             return None
#         # JSON.GET returns bytes of JSON string
#         return json.loads(data.decode())
#     except Exception as e:
#         _logger.debug("RedisJSON not available or JSON.GET failed: %s", e)
#         val = await r.get(key)
#         if val is None:
#             return None
#         return json.loads(val.decode())

# async def json_set(key, obj):
#     r = await get_redis()
#     try:
#         payload = json.dumps(obj, default=str)
#         # JSON.SET key . <payload>
#         await r.execute_command("JSON.SET", key, ".", payload)
#     except Exception as e:
#         _logger.debug("RedisJSON not available or JSON.SET failed: %s", e)
#         payload = json.dumps(obj, default=str)
#         await r.set(key, payload)


import json
import logging
from app.config import settings
import redis.asyncio as redis

_logger = logging.getLogger(__name__)

_redis = None

async def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=False)
    return _redis

async def json_get(key):
    r = await get_redis()
    try:
        data = await r.execute_command("JSON.GET", key)
        if data is None:
            return None
        return json.loads(data.decode())
    except:
        val = await r.get(key)
        return None if not val else json.loads(val.decode())

async def json_set(key, obj):
    r = await get_redis()
    payload = json.dumps(obj, default=str)
    try:
        await r.execute_command("JSON.SET", key, ".", payload)
    except:
        await r.set(key, payload)
