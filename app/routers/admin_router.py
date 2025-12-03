# Endpoints administrativos:

# GET /admin/audit/latest?count=50

# GET /admin/audit/by-user/{user_id}

from fastapi import APIRouter, Depends
from app.services import audit_service
from app.deps import get_current_actor

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/audit/latest")
async def get_latest_audit(count: int = 50, actor: str = Depends(get_current_actor)):
    # In real world validate actor roles is admin
    entries = await audit_service.read_audit_last(count)
    return {"count": len(entries), "entries": entries}
