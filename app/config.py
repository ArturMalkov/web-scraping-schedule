import pathlib
from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    name: str = Field(..., env="PROJECT_NAME")
    db_client_id: str = Field(..., env="ASTRA_DB_CLIENT_ID")
    db_client_secret: str = Field(..., env="ASTRA_DB_CLIENT_SECRET")

    class Config:
        env_file = pathlib.Path(__file__).parent.parent / ".env"


@lru_cache
def get_settings():
    return Settings()
