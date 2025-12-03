# Define convención de claves Redis y las exporta como funciones:
 
from app.config import settings

def prefs_key(user_id: str) -> str:
    return f"{settings.PREF_KEY_PREFIX}{user_id}"

def cache_key(user_id: str) -> str:
    return f"{settings.CACHE_KEY_PREFIX}{user_id}"

def ephemeral_key(user_id: str) -> str:
    return f"{settings.EPHEMERAL_KEY_PREFIX}{user_id}"

def audit_stream_key() -> str:
    return settings.AUDIT_STREAM_KEY

def delete_flag_key(user_id: str) -> str:
    return f"{settings.DELETE_FLAG_PREFIX}{user_id}"

def anonymize_flag_key(user_id: str) -> str:
    return f"{settings.ANON_FLAG_PREFIX}{user_id}"
