import enum
from sqlalchemy import Column, String, Enum, Integer

from core.models import Base


class ProviderType(enum.Enum):
    AIMLAPI = "AIMLAPI"


class AIProvider(Base):
    name = Column(String, unique=True, index=True)
    api_url = Column(String)
    api_key = Column(String)
    priority = Column(Integer)
    provider_type = Column(Enum(ProviderType))
