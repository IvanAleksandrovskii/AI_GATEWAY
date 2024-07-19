from pydantic import BaseModel


class Message(BaseModel):
    content: str
    # TODO: source is unused
    source: str


class Response(BaseModel):
    request_content: str
    content: str
    ai_model: str
