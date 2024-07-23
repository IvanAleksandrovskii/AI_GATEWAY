from sqlalchemy import Column, String, Integer
from typing import Dict, Any, Optional

from core.models import Base


class AIProvider(Base):
    name = Column(String, unique=True, index=True)
    api_url = Column(String)
    api_key = Column(String)
    priority = Column(Integer)

    # TODO: wrote only for two service I have (one is OpenAI and it's not payed), need to improve
    def get_request_payload(self, message: str) -> Dict[str, Any]:
        """
        Get request payload for the specified AI provider

        :param message: The message to send to the AI provider.
        :return: The request payload as a dictionary.
        :raises ValueError: If the AI provider is not supported.
        """
        if self.name == "OpenAI" or self.name == "AIMLapi":
            return {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": message}]
            }
        else:
            raise ValueError(f"Unsupported AI provider: {self.name}")

    def get_headers(self) -> Dict[str, str]:
        """
        Construct the headers for the AI provider's API request.

        :return: A dictionary containing the authorization header.
        """
        return {"Authorization": f"Bearer {self.api_key}"}

# TODO: for both OpenAI and AIMLapi is the same (as docs says), need to improve
    def parse_response(self, response_data: Dict[str, Any]) -> Optional[str]:
        """
        Parse the response from the AI provider.

        :param response_data: The response data as a dictionary.
        :return: The parsed response content as a string, or None if parsing fails.
        """
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
