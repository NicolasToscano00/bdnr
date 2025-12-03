# import uvicorn
# from fastapi import FastAPI
# from app.routers import privacy_router, admin_router

# app = FastAPI(title="Privacy & Security - Redis-only Storage")

# app.include_router(privacy_router.router)
# app.include_router(admin_router.router)

# @app.get("/")
# async def root():
#     return {"service": "privacy-redis", "status": "ok"}

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


from fastapi import FastAPI
from app.routers.privacy_router import router as privacy_router

app = FastAPI(title="Privacy & Security - Redis")

app.include_router(privacy_router)

@app.get("/")
def root():
    return {"status": "running"}
