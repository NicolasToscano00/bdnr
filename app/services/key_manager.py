# Genera claves efímeras (AES-GCM).

# Las guarda con TTL.

# Devuelve la clave al sistema para cifrar datos sensibles.

import base64
import datetime
from app.db.redis_cluster import get_redis
from app.db.key_spaces import ephemeral_key
from app.config import settings
from app.utils.crypto import gen_aes_key, key_to_b64, b64_to_key


async def create_ephemeral_key_for_user(user_id: str, ttl: int = None) -> str:
    """
    Creates an ephemeral AES key and stores it in Redis with TTL.
    Returns the redis key name (not the raw key).
    """
    if ttl is None:
        ttl = settings.EPHEMERAL_KEY_TTL
    key = gen_aes_key()
    b64 = key_to_b64(key)
    redis_key = ephemeral_key(user_id)
    r = await get_redis()
    # store base64 string
    await r.set(redis_key, b64.encode(), ex=ttl)
    return redis_key

async def get_ephemeral_key(user_id: str):
    r = await get_redis()
    redis_key = ephemeral_key(user_id)
    val = await r.get(redis_key)
    if not val:
        return None
    if isinstance(val, bytes):
        val = val.decode()
    return b64_to_key(val)
