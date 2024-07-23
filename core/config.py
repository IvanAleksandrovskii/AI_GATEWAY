import logging
import os

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

from dotenv import load_dotenv


load_dotenv(".env")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_POOL_SIZE = int(os.getenv("POSTGRES_POOL_SIZE"))
POSTGRES_MAX_OVERFLOW = int(os.getenv("POSTGRES_MAX_OVERFLOW"))

APP_RUN_HOST = str(os.getenv("APP_RUN_HOST"))
APP_RUN_PORT = int(os.getenv("APP_RUN_PORT"))
DEBUG = os.getenv("DEBUG", "False").lower() in ('true', '1')

TOKEN_EXPIRATION_DAYS = int(os.getenv("TOKEN_EXPIRATION_DAYS", "30"))

HTTP_CLIENT_TIMEOUT = int(os.getenv("HTTP_CLIENT_TIMEOUT", "300"))
HTTP_CLIENTS_MAX_KEEPALIVE_CONNECTIONS = int(os.getenv("HTTP_CLIENTS_MAX_KEEPALIVE_CONNECTIONS", "10"))


class RunConfig(BaseModel):
    host: str = APP_RUN_HOST
    port: int = APP_RUN_PORT
    debug: bool = DEBUG


class APIConfig(BaseModel):
    prefix: str = "/api"


class DBConfig(BaseModel):
    url: PostgresDsn = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@pg:5432/{POSTGRES_DB}"
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
    expiration_days: int = TOKEN_EXPIRATION_DAYS


class HTTPClientConfig(BaseModel):
    timeout: int = HTTP_CLIENT_TIMEOUT
    max_keepalive_connections: int = HTTP_CLIENTS_MAX_KEEPALIVE_CONNECTIONS


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: APIConfig = APIConfig()
    db: DBConfig = DBConfig()
    token: TokenConfig = TokenConfig()
    http_client: HTTPClientConfig = HTTPClientConfig()


settings = Settings()


# Setup logging
def setup_logging() -> logging.Logger:
    """
    Set up logging configuration.

    :return: Configured logger
    """
    log_level = logging.DEBUG if settings.run.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    new_logger = logging.getLogger()

    # Hide too many logging information
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    return new_logger


logger = setup_logging()
logger.info(f"Debug mode: {settings.run.debug}")
# TODO: Split out and set default false for db echo settings, set fasle for default and
#  write this is optional value in .env and docker-compose
logger.debug(f"Database URL: {settings.db.url}")
