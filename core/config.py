from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    # TODO: for now debug is unused
    debug: bool = False


class APIConfig(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: APIConfig = APIConfig()
    # db_url: str


settings = Settings()
