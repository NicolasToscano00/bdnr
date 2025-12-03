# # Escribe eventos en Redis Stream.

# # Lectura opcional con paginado.

# import datetime
# import json
# from app.db.redis_cluster import get_redis
# from app.db.key_spaces import audit_stream_key
# from app.models.schemas import AuditEvent

# async def write_audit_event(event: AuditEvent):
#     r = await get_redis()
#     data = {
#         "user_id": event.user_id,
#         "actor": event.actor,
#         "action": event.action,
#         "details": json.dumps(event.details or {}),
#         "timestamp": (event.timestamp or datetime.datetime.utcnow()).isoformat()
#     }
#     # xadd requires mapping of field->value; values must be bytes
#     await r.xadd(audit_stream_key(), data)

# async def read_audit_last(count: int = 50):
#     r = await get_redis()
#     # XRANGE - get last N can be done with XREVRANGE in newer versions; using xrange from "-" to "+"
#     # We'll use XREVRANGE if available; fallback to XRANGE and slice.
#     try:
#         entries = await r.execute_command("XREVRANGE", audit_stream_key(), "+", "-", "COUNT", str(count))
#         # entries = list of [id, [field, value, ...]]
#         parsed = []
#         for entry in entries:
#             _id = entry[0].decode()
#             pairs = entry[1]
#             d = {}
#             for i in range(0, len(pairs), 2):
#                 k = pairs[i].decode()
#                 v = pairs[i+1].decode()
#                 d[k] = v
#             parsed.append({"id": _id, **d})
#         return parsed
#     except Exception:
#         # Fallback: XRANGE
#         entries = await r.xrange(audit_stream_key(), min="-", max="+")
#         last = entries[-count:] if len(entries) > count else entries
#         parsed = []
#         for entry in last[::-1]:
#             _id = entry[0].decode()
#             pairs = entry[1]
#             d = {}
#             for k, v in pairs.items():
#                 key = k.decode() if isinstance(k, bytes) else k
#                 val = v.decode() if isinstance(v, bytes) else v
#                 d[key] = val
#             parsed.append({"id": _id, **d})
#         return parsed


from app.db.redis_cluster import get_redis
import json
import time

AUDIT_STREAM = "audit_log"

async def write_audit(user_id: str, action: str, details: dict):
    r = await get_redis()
    entry = {
        "timestamp": str(time.time()),
        "user_id": user_id,
        "action": action,
        "details": json.dumps(details),
    }
    await r.xadd(AUDIT_STREAM, entry)
