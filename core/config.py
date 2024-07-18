from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    # TODO: unused now
    debug: bool = True


class APIConfig(BaseModel):
    prefix: str = "/api"


class DBConfig(BaseModel):
    url: PostgresDsn
    debug: bool = True
    pool_size: int = 5
    max_overflow: int = 10


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: APIConfig = APIConfig()
    db: DBConfig


settings = Settings()
