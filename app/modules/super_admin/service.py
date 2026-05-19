from datetime import datetime, timezone
from typing import Optional, Tuple
from uuid import UUID 
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import (verify_password,get_password_hash,create_access_token,create_refresh_token,decode_token)
from app.modules.super_admin.model import SuperAdmin
from app.modules.super_admin.repository import SuperAdminAuthRepository
from app.modules.super_admin.schemas import SuperAdminRegister, SuperAdminLogin
from app.modules.auth.schemas import Token

settings = get_settings()

class SuperAdminService:
    def __init__(self) -> None:
        self.super_admin_repo = SuperAdminAuthRepository()
        
    def _create_token(self, subject:str, role:str) -> Token:
        access_token = create_access_token(subject)
        refresh_token = create_refresh_token(subject)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        
    async def register_super_admin(self,db:AsyncSession, data:SuperAdminRegister) ->Tuple[SuperAdmin,Token]:
        if data.registration_secret != settings.SUPER_ADMIN_SECRET:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid registration code")
        
        if await self.super_admin_repo.super_admin_exists(db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Superadmin already exist")
        
        existing = await self.super_admin_repo.get_super_admin_by_email(db, data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered",)
        
        admin=SuperAdmin(
            email=data.email,
            password_hash=get_password_hash(data.password),
             first_name=data.first_name,
            last_name=data.last_name,
            is_active=True,
        )
        db.add(admin)
        await db.flush()
        await db.commit()
        await db.refresh(admin)
        
        tokens = self._create_token(str(admin.id),"super_admin")
        return admin, tokens
        
    async def login_super_admin(self,db:AsyncSession, data:SuperAdminLogin)-> Tuple[SuperAdmin,Token]:
        admin = await self.super_admin_repo.get_super_admin_by_email(db,data.email)
        
        if not admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incalid email or password")
        
        if not admin.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")
        
        if not verify_password(data.password, admin.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")
        
        admin.last_login = datetime.now(timezone.utc)
        await db.flush()
        
        tokens = self._create_token(str(admin.id),"super_admin")
        return admin,tokens
    
    async def logout(self,token:str)-> None:
        pass
    
    async def refresh_token(self, db: AsyncSession, refresh_token: str) -> Token:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # Try super admin first, then user
        admin = await self.super_admin_repo.get_super_admin_by_id(db, UUID(user_id))
        if admin:
            tokens = self._create_token(str(admin.id), "super_admin")
            return tokens


        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )