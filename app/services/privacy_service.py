# # Lee y escribe preferencias en RedisJSON.

# # Invalida caché tras un update.

# # Llama a audit service para registrar.

# import datetime
# import json
# from typing import Optional
# from app.db.key_spaces import prefs_key, cache_key
# from app.db.redis_cluster import json_get, json_set, get_redis
# from app.config import settings
# from app.models.schemas import PrivacyPreferences, UpdatePreferencesRequest, AuditEvent
# from app.services import audit_service, key_manager

# async def get_preferences(user_id: str) -> Optional[PrivacyPreferences]:
#     r = await get_redis()
#     ckey = cache_key(user_id)
#     cached = await r.get(ckey)
#     if cached:
#         try:
#             data = json.loads(cached.decode() if isinstance(cached, bytes) else cached)
#             return PrivacyPreferences(**data)
#         except Exception:
#             pass
#     # read JSON doc (RedisJSON or fallback)
#     key = prefs_key(user_id)
#     doc = await json_get(key)
#     if doc is None:
#         return None
#     # pydantic conversion
#     prefs = PrivacyPreferences(**doc)
#     # store in cache
#     await r.set(ckey, json.dumps(prefs.dict(), default=str).encode(), ex=settings.PREF_CACHE_TTL)
#     return prefs

# async def upsert_preferences(user_id: str, update: dict, actor: str):
#     key = prefs_key(user_id)
#     now = datetime.datetime.utcnow().isoformat()
#     existing = await json_get(key)
#     if existing is None:
#         existing = {"user_id": user_id, "created_at": now}
#     # update allowed fields
#     for k, v in update.items():
#         existing[k] = v
#     existing["updated_at"] = now
#     # Save
#     await json_set(key, existing)
#     # invalidate cache
#     r = await get_redis()
#     await r.delete(cache_key(user_id))
#     # Audit
#     evt = AuditEvent(user_id=user_id, actor=actor, action="update_preferences", details=update, timestamp=datetime.datetime.utcnow())
#     await audit_service.write_audit_event(evt)

# async def request_delete_user_data(user_id: str, actor: str):
#     r = await get_redis()
#     flag = f"{settings.DELETE_FLAG_PREFIX}{user_id}"
#     await r.set(flag, "1")
#     # Audit
#     evt = AuditEvent(user_id=user_id, actor=actor, action="request_delete", details={"flag_key": flag}, timestamp=datetime.datetime.utcnow())
#     await audit_service.write_audit_event(evt)
#     # Immediately trigger anonymize pipeline (for demo we run inline)
#     await anonymize_user(user_id, actor)

# async def anonymize_user(user_id: str, actor: str):
#     """
#     Inline anonymization pipeline:
#     - read prefs doc
#     - remove sensitive fields or replace with placeholders
#     - write doc back
#     - audit
#     """
#     key = prefs_key(user_id)
#     doc = await json_get(key)
#     if doc is None:
#         return
#     # Replace sensitive fields if present
#     sensitive = doc.get("sensitive_fields", {})
#     for field, meta in list(sensitive.items()):
#         # if field contained encrypted data, remove
#         sensitive[field] = {"anonymized": True, "replaced_at": datetime.datetime.utcnow().isoformat()}
#     if sensitive:
#         doc["sensitive_fields"] = sensitive
#     # set anonymize flag
#     doc["anonymized_at"] = datetime.datetime.utcnow().isoformat()
#     await json_set(key, doc)
#     # invalidate cache
#     r = await get_redis()
#     await r.delete(cache_key(user_id))
#     evt = AuditEvent(user_id=user_id, actor=actor, action="anonymize_user", details={"fields": list(sensitive.keys())}, timestamp=datetime.datetime.utcnow())
#     await audit_service.write_audit_event(evt)

# async def store_sensitive_field(user_id: str, field_name: str, plaintext: bytes, actor: str):
#     """
#     Example: store an encrypted sensitive field using an ephemeral key.
#     - create ephemeral key (ttl)
#     - encrypt plaintext
#     - store encrypted blob under sensitive_fields in JSON doc referencing key id
#     """
#     # generate ephemeral key for user
#     key_id = await key_manager.create_ephemeral_key_for_user(user_id)
#     # get raw key bytes
#     raw_key = await key_manager.get_ephemeral_key(user_id)
#     from app.utils.crypto import encrypt_bytes, key_to_b64
#     enc = encrypt_bytes(plaintext, raw_key)
#     # build metadata to store
#     meta = {
#         "ciphertext": enc["ciphertext"],
#         "nonce": enc["nonce"],
#         "key_id": key_id,
#         "stored_at": datetime.datetime.utcnow().isoformat()
#     }
#     # store into user's JSON doc
#     key = prefs_key(user_id)
#     doc = await json_get(key) or {"user_id": user_id, "created_at": datetime.datetime.utcnow().isoformat()}
#     sensitive = doc.get("sensitive_fields", {})
#     sensitive[field_name] = meta
#     doc["sensitive_fields"] = sensitive
#     doc["updated_at"] = datetime.datetime.utcnow().isoformat()
#     await json_set(key, doc)
#     # audit
#     evt = AuditEvent(user_id=user_id, actor=actor, action="store_sensitive_field", details={"field": field_name}, timestamp=datetime.datetime.utcnow())
#     await audit_service.write_audit_event(evt)


from app.db.redis_cluster import json_get, json_set
from app.crypto.aes import encrypt_sensitive, decrypt_sensitive
from app.services.audit_service import write_audit
from app.models.privacy import PrivacySettings, PrivacyResponse

async def get_privacy(user_id: str) -> PrivacyResponse | None:
    key = f"user:{user_id}:privacy"
    data = await json_get(key)

    if not data:
        return None

    if data.get("sensitive_note"):
        data["sensitive_note"] = decrypt_sensitive(data["sensitive_note"])

    return PrivacyResponse(user_id=user_id, settings=PrivacySettings(**data))

async def update_privacy(user_id: str, settings: PrivacySettings):
    key = f"user:{user_id}:privacy"
    data = settings.dict()

    if data.get("sensitive_note"):
        data["sensitive_note"] = encrypt_sensitive(data["sensitive_note"])

    await json_set(key, data)

    await write_audit(user_id, "UPDATE_PRIVACY", data)

    return {"status": "ok"}

async def delete_privacy(user_id: str):
    key = f"user:{user_id}:privacy"
    from app.db.redis_cluster import get_redis
    r = await get_redis()
    await r.delete(key)

    await write_audit(user_id, "DELETE_PRIVACY", {})
    return {"status": "deleted"}
