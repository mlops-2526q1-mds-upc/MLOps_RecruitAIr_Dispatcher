from datetime import datetime

from pydantic import BaseModel, Field

from ...database.models import JobOfferStatus


class JobOfferSchema(BaseModel):
    created_at: datetime = Field(
        ..., description="Timestamp when the job offer was created", examples=["2025-12-01T13:56:26.136274+00:00"]
    )
    id: int = Field(..., description="Unique identifier for the job offer", examples=[1])
    status: JobOfferStatus = Field(
        ..., description="Current status of the job offer", examples=[JobOfferStatus.PENDING]
    )
    text: str = Field(
        ...,
        description="Text description of the job offer",
        examples=["Looking for a software engineer with experience in Python and FastAPI."],
    )


class ApplicantSchema(BaseModel):
    created_at: datetime = Field(
        ..., description="Timestamp when the applicant was created", examples=["2025-12-01T13:56:26.136274+00:00"]
    )
    id: int = Field(..., description="Unique identifier for the applicant", examples=[1])
    cv: str = Field(
        ...,
        description="Curriculum Vitae of the applicant in text format",
        examples=["Experienced software engineer with a background in AI."],
    )
    offer_id: int = Field(..., description="Identifier of the associated job offer", examples=[1])


class CriterionSchema(BaseModel):
    id: int = Field(..., description="Unique identifier for the criterion", examples=[1])
    description: str = Field(
        ...,
        description="Description of the extracted criterion from the job offer",
        examples=["Experience with Python programming."],
    )
    importance: float = Field(
        ...,
        description="Importance of the extracted criterion on a scale from 0 to 1",
        ge=0,
        le=1,
        examples=[0.8],
    )
    offer_id: int = Field(..., description="Identifier of the associated job offer", examples=[1])


class ApplicantScoreSchema(BaseModel):
    criteria_id: int = Field(..., description="Identifier of the associated criterion", examples=[1])
    applicant_id: int = Field(..., description="Identifier of the associated applicant", examples=[1])
    score: float = Field(
        ...,
        description="Score assigned to the applicant for the given criterion on a scale from 0 to 10",
        ge=0,
        le=10,
        examples=[8.5],
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the score was created", examples=["2025-12-01T13:56:26.136274+00:00"]
    )
