import os

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from dotenv import load_dotenv


load_dotenv(".env")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    # TODO: unused now
    debug: bool = True


class APIConfig(BaseModel):
    prefix: str = "/api"


class DBConfig(BaseModel):
    url: PostgresDsn = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@0.0.0.0:5432/{POSTGRES_DB}"
    # URL for migrations
    url_sync: PostgresDsn = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@0.0.0.0:5432/{POSTGRES_DB}"
    debug: bool = True
    pool_size: int = 5
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: APIConfig = APIConfig()
    db: DBConfig = DBConfig()


settings = Settings()

if settings.db.debug:
    # TODO: prints in debug mode with every every time file uses settings as import runs.
    #  For project start purposes keeping it for now here
    print(f"Database URL: {settings.db.url} \n"
          f"Database URL sync (used for migrations): {settings.db.url_sync}")
