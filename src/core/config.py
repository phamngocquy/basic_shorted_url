# coding=utf-8
import logging
import secrets
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings

__author__ = 'qPham'
_logger = logging.getLogger(__name__)
env_location = Path("./.env").resolve()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'uLink'
    API_STR: str = ''
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    REDIS_HOST: str
    BACKEND_CORS_ORIGINS: str
    SQLALCHEMY_DATABASE_URI: str

    LENGTH_SHORTEN_TOKEN: int

    API_KEY: str

    DOMAIN_NAME: str

    API_DOCS: Optional[str]
    API_REDOC: Optional[str]
    PROXY_IP: Optional[str]


settings = Settings(
    _env_file=env_location,
    _env_file_encoding="utf-8"
)
