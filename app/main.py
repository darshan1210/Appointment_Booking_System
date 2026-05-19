# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy import text               # <-- new import
import time

from app.core.config import get_settings
from app.db.database import engine, Base   # Base no longer needed
from app.core.logging import Logger
from app.api.v1.api import api_router
from app.middleware.security_middleware import SecurityHeadersMiddleware

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    Logger.info("🚀 Starting up Project...")
    Logger.info("✅ Application started (no table creation)")
    yield
    Logger.info("🛑 Shutting down Project Management API...")

app = FastAPI(
    title="Appointment Booking system",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(SecurityHeadersMiddleware)
# ... (keep your CORS, exception handlers, etc. unchanged)


app.include_router(api_router, prefix=settings.API_V1_STR)



@app.get("/health", tags=["Health"])
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0",
            "timestamp": time.time(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": str(e),
                "version": "1.0.0",
                "timestamp": time.time(),
            },
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)