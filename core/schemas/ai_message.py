from pydantic import BaseModel


class Message(BaseModel):
    content: str


class Response(BaseModel):
    request_content: str
    content: str
    ai_model: str
