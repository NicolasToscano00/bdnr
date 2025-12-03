from pydantic import BaseModel

class PrivacySettings(BaseModel):
    share_profile: bool
    share_activity: bool
    store_history: bool
    sensitive_note: str | None = None  # este se cifra

class PrivacyResponse(BaseModel):
    user_id: str
    settings: PrivacySettings
