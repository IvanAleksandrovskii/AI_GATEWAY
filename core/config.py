import os

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from dotenv import load_dotenv


load_dotenv(".env")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DEBUG = bool(os.getenv("POSTGRES_DEBUG"))
POSTGRES_POOL_SIZE = int(os.getenv("POSTGRES_POOL_SIZE"))
POSTGRES_MAX_OVERFLOW = int(os.getenv("POSTGRES_MAX_OVERFLOW"))

APP_RUN_HOST = str(os.getenv("APP_RUN_HOST"))
APP_RUN_PORT = int(os.getenv("APP_RUN_PORT"))
DEBUG = bool(os.getenv("DEBUG"))

TOKEN_EXPIRATION_MINUTES = int(os.getenv("TOKEN_EXPIRATION_MINUTES"))
# TODO: unused now
TOKEN_EXPIRATION_DAYS = int(os.getenv("TOKEN_EXPIRATION_DAYS", "30"))


class RunConfig(BaseModel):
    host: str = APP_RUN_HOST
    port: int = APP_RUN_PORT
    # TODO: unused now
    debug: bool = DEBUG


class APIConfig(BaseModel):
    prefix: str = "/api"


class DBConfig(BaseModel):
    url: PostgresDsn = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@pg:5432/{POSTGRES_DB}"
    debug: bool = POSTGRES_DEBUG
    pool_size: int = POSTGRES_POOL_SIZE
    max_overflow: int = POSTGRES_MAX_OVERFLOW

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class TokenConfig(BaseModel):
    expiration_minutes: int = TOKEN_EXPIRATION_MINUTES
    # TODO: unused now
    expiration_days: int = TOKEN_EXPIRATION_DAYS


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: APIConfig = APIConfig()
    db: DBConfig = DBConfig()
    token: TokenConfig = TokenConfig()


settings = Settings()

if settings.db.debug:
    # TODO: prints in debug mode with every every time file uses settings as import runs.
    #  For project start purposes keeping it for now here
    print(f"Database URL: {settings.db.url}")
