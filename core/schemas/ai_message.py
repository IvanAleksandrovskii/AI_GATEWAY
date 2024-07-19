from pydantic import BaseModel


class Message(BaseModel):
    content: str
    source: str


class Response(BaseModel):
    content: str
    ai_model: str
