from pydantic import Field, HttpUrl

from ..common_settings import BaseWorkerSettings


class ExtractorWorkerSettings(BaseWorkerSettings):
    extractor_api_base_url: HttpUrl = Field(..., description="Base URL for the extractor API endpoint")
    extractor_api_bearer_token: str = Field(..., description="Bearer token for authenticating with the extractor API")
    http_timeout: int = Field(30, description="HTTP timeout in seconds for requests to the extractor API")
