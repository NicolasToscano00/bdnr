from fastapi import Header, HTTPException

async def get_current_actor(x_actor: str = Header(None)):
    """
    Simulated auth: in production replace with JWT + roles check.
    Provide header: X-Actor: user_or_admin
    """
    if not x_actor:
        raise HTTPException(status_code=401, detail="Missing X-Actor header")
    return x_actor
