from pydantic import Field, HttpUrl

from ..common_settings import BaseWorkerSettings


class EvaluatorWorkerSettings(BaseWorkerSettings):
    evaluator_api_base_url: HttpUrl = Field(..., description="Base URL for the evaluator API endpoint")
    evaluator_api_bearer_token: str = Field(..., description="Bearer token for authenticating with the evaluator API")
    http_timeout: int = Field(30, description="HTTP timeout in seconds for requests to the evaluator API")
