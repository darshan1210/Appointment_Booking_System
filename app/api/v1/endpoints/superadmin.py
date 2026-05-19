from fastapi import APIRouter,Depends,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.modules.super_admin.service import SuperAdminService

from app.modules.super_admin.schemas import (SuperAdminLogin, SuperAdminRegister)
from app.modules.auth.schemas import (Token)

router = APIRouter()
superadmin_auth_service = SuperAdminService()
security = HTTPBearer()


@router.post("/super-admin/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_super_admin(
    data: SuperAdminRegister,
    db: AsyncSession = Depends(get_db),
):
    """Register a new Super Admin (requires secret code)."""
    _, tokens = await superadmin_auth_service.register_super_admin(db, data)
    return tokens


@router.post("/super-admin/login", response_model=Token)
async def login_super_admin(
    data: SuperAdminLogin,
    db: AsyncSession = Depends(get_db),
):
    """Super Admin login."""
    _, tokens = await superadmin_auth_service.login_super_admin(db, data)
    return tokens
