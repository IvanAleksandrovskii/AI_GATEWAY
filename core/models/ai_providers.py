from sqlalchemy import Column, String, Integer
from typing import Dict, Any, Optional

from core.models import Base


class AIProvider(Base):
    name = Column(String, unique=True, index=True)
    api_url = Column(String)
    api_key = Column(String)
    priority = Column(Integer)

    # TODO: wrote only for one service I have, need to improve
    def get_request_payload(self, message: str) -> Dict[str, Any]:
        return {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message}]
        }

    def get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def parse_response(self, response_data: Dict[str, Any]) -> Optional[str]:
        try:
            return response_data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return None

    # TODO: not used part down below
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "api_url": self.api_url,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIProvider':
        return cls(**data)

    def __repr__(self) -> str:
        return f"<AIProvider(name='{self.name}', priority={self.priority})>"
