import importlib.metadata
import os
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from ..database import get_db_session

SessionDep = Annotated[Session, Depends(get_db_session)]

tags_metadata = [
    {"name": "Job Offers", "description": "Operations related to job offers."},
    {"name": "Criteria", "description": "Operations related to criteria extracted from job offers."},
    {"name": "Applicants", "description": "Operations related to applicants applying for job offers."},
    {"name": "Scores", "description": "Operations related to scores assigned to applicants based on criteria."},
    {"name": "Health", "description": "Health check endpoint."},
]

try:
    app_version = importlib.metadata.version("recruitair")
except importlib.metadata.PackageNotFoundError:
    import pathlib
    import tomllib

    pyproject_path = pathlib.Path(__file__).parent.parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        pyproject_data = tomllib.load(f)
    app_version = pyproject_data["project"]["version"]

api_root_path = os.getenv("RECRUITAIR_API_ROOT_PATH", "")

app = FastAPI(title="RecruitAIr API", version=app_version, openapi_tags=tags_metadata, root_path=api_root_path)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


from .resources import *
