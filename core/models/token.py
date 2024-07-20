from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from core.models import Base


class Token(Base):
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
