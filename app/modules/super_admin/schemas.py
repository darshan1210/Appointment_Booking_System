from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel,EmailStr, Field, ConfigDict


class SuperAdminRegister(BaseModel):
    email:EmailStr
    password:str= Field(..., min_length=8, max_length=128)
    first_name:Optional[str]=Field(None,max_length=100)
    last_name:Optional[str]=Field(None, max_length=100)
    registration_secret:str=Field(..., min_length=1)



class SuperAdminLogin(BaseModel):
    email: EmailStr
    password: str


class SuperAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime