from fastapi import APIRouter

from app.api.v1.endpoints import superadmin

api_router = APIRouter()

api_router.include_router(superadmin.router, prefix="/auth", tags=["Authentication"])