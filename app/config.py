# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     REDIS_URL: str = "redis://localhost:6379/0"
#     PREF_CACHE_TTL: int = 30           # seconds for cache
#     EPHEMERAL_KEY_TTL: int = 300       # seconds for ephemeral keys
#     AUDIT_STREAM_KEY: str = "audit:stream"
#     PREF_KEY_PREFIX: str = "privacy:prefs:"
#     CACHE_KEY_PREFIX: str = "privacy:cache:"
#     EPHEMERAL_KEY_PREFIX: str = "ek:"
#     DELETE_FLAG_PREFIX: str = "privacy:delete_request:"
#     ANON_FLAG_PREFIX: str = "privacy:anonymize:"
#     ENV_FILE: str = ".env"
#     class Config:
#         env_file = ".env"

# settings = Settings()

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"

    # AES-GCM master key (en una app real va en Vault)
    AES_MASTER_KEY: str = "00112233445566778899AABBCCDDEEFF"

    class Config:
        env_file = ".env"

settings = Settings()
