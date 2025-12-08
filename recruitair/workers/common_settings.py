from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseWorkerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RECRUITAIR_")

    db_username: str = Field(..., description="Database username")
    db_password: str = Field(..., description="Database password")
    db_host: str = Field(..., description="Database host")
    db_port: int = Field(5432, description="Database port")
    db_database: str = Field(..., description="Database name")

    batch_size: int = Field(100, description="Number of tasks to process in a batch")
    interval_seconds: int = Field(10, description="Interval between task processing in seconds")

    metrics_server_port: int = Field(8000, description="Port on which to expose Prometheus metrics")
    expose_metrics: bool = Field(False, description="Whether to expose Prometheus metrics")
