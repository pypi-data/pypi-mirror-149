import secrets
import urllib.parse
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


def url_quote(string: str) -> str:
    return urllib.parse.quote_plus(string)


class Settings(BaseSettings):
    VERSION = '1.0.0'
    API_PREFIX: str = ""
    LOG_LEVEL: str = 'DEBUG'

    PROJECT_NAME: str = "CS5800 Group 2 Final Project"

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = '5432'
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    ALEMBIC_CONNECTION_STRING: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=url_quote(values.get("POSTGRES_USER")),
            password=url_quote(values.get("POSTGRES_PASSWORD")),
            host=url_quote(values.get("POSTGRES_SERVER")),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
