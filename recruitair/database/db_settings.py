from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RECRUITAIR_")
    db_username: Optional[str] = Field(None, description="Database username")
    db_password: Optional[str] = Field(None, description="Database password")
    db_host: Optional[str] = Field(None, description="Database host address")
    db_port: Optional[int] = Field(None, description="Database port number")
    db_database: Optional[str] = Field(None, description="Database name or path to the SQLite file")
    db_driver: str = "postgresql"
    db_async_driver: str = "postgresql+asyncpg"
