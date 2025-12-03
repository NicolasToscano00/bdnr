from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class PrivacyPreferences(BaseModel):
    user_id: str
    share_email: bool = False
    share_progress: bool = True
    anonymize_activity: bool = False
    sensitive_fields: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UpdatePreferencesRequest(BaseModel):
    share_email: Optional[bool] = None
    share_progress: Optional[bool] = None
    anonymize_activity: Optional[bool] = None

class AuditEvent(BaseModel):
    user_id: str
    actor: str
    action: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
