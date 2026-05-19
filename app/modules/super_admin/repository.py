from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.super_admin.model import SuperAdmin


class SuperAdminAuthRepository:
    @staticmethod
    async def get_super_admin_by_email(db:AsyncSession, email:str)-> Optional[SuperAdmin]:
        result = await db.execute(select(SuperAdmin).where(SuperAdmin.email == email))
        return result.scalar_one_or_none()
        
    
    @staticmethod
    async def get_super_admin_by_id(db: AsyncSession, admin_id) -> Optional[SuperAdmin]:
        result = await db.execute(select(SuperAdmin).where(SuperAdmin.id == admin_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def super_admin_exists(db: AsyncSession) -> bool:
        result = await db.execute(select(SuperAdmin)) 
        return result.scalar_one_or_none() is not None

