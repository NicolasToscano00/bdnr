# # Endpoints:

# # GET /privacy/prefs/{user_id}

# # PUT /privacy/prefs/{user_id}

# # POST /privacy/delete/{user_id}

# # POST /privacy/anonymize/{user_id}

# from fastapi import APIRouter, Depends, HTTPException
# from app.models.schemas import PrivacyPreferences, UpdatePreferencesRequest
# from app.services import privacy_service
# from app.deps import get_current_actor

# router = APIRouter(prefix="/privacy", tags=["privacy"])

# @router.get("/prefs/{user_id}", response_model=PrivacyPreferences)
# async def get_prefs(user_id: str):
#     prefs = await privacy_service.get_preferences(user_id)
#     if prefs is None:
#         raise HTTPException(status_code=404, detail="Preferences not found")
#     return prefs

# @router.put("/prefs/{user_id}")
# async def put_prefs(user_id: str, req: UpdatePreferencesRequest, actor: str = Depends(get_current_actor)):
#     data = {k:v for k,v in req.dict().items() if v is not None}
#     if not data:
#         raise HTTPException(status_code=400, detail="No fields to update")
#     await privacy_service.upsert_preferences(user_id, data, actor)
#     return {"status": "ok"}

# @router.post("/store-sensitive/{user_id}/{field_name}")
# async def store_sensitive(user_id: str, field_name: str, body: dict, actor: str = Depends(get_current_actor)):
#     # Accepts JSON {"value": "string to protect"}
#     val = body.get("value")
#     if val is None:
#         raise HTTPException(status_code=400, detail="Missing value")
#     await privacy_service.store_sensitive_field(user_id, field_name, val.encode(), actor)
#     return {"status":"stored"}

# @router.post("/request-delete/{user_id}")
# async def request_delete(user_id: str, actor: str = Depends(get_current_actor)):
#     await privacy_service.request_delete_user_data(user_id, actor)
#     return {"status":"delete_requested"}

# @router.post("/anonymize/{user_id}")
# async def anonymize_endpoint(user_id: str, actor: str = Depends(get_current_actor)):
#     await privacy_service.anonymize_user(user_id, actor)
#     return {"status":"anonymized"}


from fastapi import APIRouter
from app.models.privacy import PrivacySettings
from app.services.privacy_service import (
    get_privacy,
    update_privacy,
    delete_privacy,
)

router = APIRouter(prefix="/privacy", tags=["privacy"])

@router.get("/{user_id}")
async def read_privacy(user_id: str):
    return await get_privacy(user_id)

@router.post("/{user_id}")
async def write_privacy(user_id: str, settings: PrivacySettings):
    return await update_privacy(user_id, settings)

@router.delete("/{user_id}")
async def remove_privacy(user_id: str):
    return await delete_privacy(user_id)
