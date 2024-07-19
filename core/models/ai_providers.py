from sqlalchemy import Column, String, Integer
from core.models import Base


class AIProvider(Base):
    name = Column(String, unique=True, index=True)
    api_url = Column(String)
    api_key = Column(String)
    priority = Column(Integer)
