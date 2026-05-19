import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class SuperAdmin(Base):
    __tablename__ = "super_admins"
    
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    email:Mapped[str]=mapped_column(String(255), unique=True, nullable=False , index=True)
    password_hash:Mapped[str]= mapped_column(String(255), nullable=False)
    first_name:Mapped[Optional[str]]= mapped_column(String(100), nullable=False)
    last_name:Mapped[Optional[str]]= mapped_column(String(100), nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean, default=True, nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"), onupdate=text("now()"), nullable=False)
    