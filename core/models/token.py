from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

from core.models import Base


class Token(Base):
    value = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    @hybrid_property
    def is_active(self):
        """
        Check if the token is active by comparing its expiration time with the current time.

        :return: Boolean indicating if the token is active
        """
        return self.expires_at > datetime.now(timezone.utc)
