# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text               # <-- new import
import logging
import time

from app.core.config import get_settings
from app.db.database import engine, supabase  # Base no longer needed

settings = get_settings()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("🚀 Starting up Project...")
    # ❌ Removed: Base.metadata.create_all(bind=engine)  <-- no table creation
    logger.info("✅ Application started (no table creation)")
    yield
    logger.info("🛑 Shutting down Project Management API...")

app = FastAPI(
    title="Appointment Booking system",
    version="1.0.0",
    lifespan=lifespan,
)

# ... (keep your CORS, exception handlers, etc. unchanged)

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check that verifies connectivity to the Supabase database.
    Returns 200 if the database is reachable, 503 otherwise.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = f"error: {str(e)}"
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": db_status,
                "version": "1.0.0",
                "timestamp": time.time(),
            },
        )
    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0",
        "timestamp": time.time(),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)