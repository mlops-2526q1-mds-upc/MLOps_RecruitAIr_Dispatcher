from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


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


class ApplicantScore(Base):
    __tablename__ = "applicant_scores"

    criteria_id = Column(Integer, ForeignKey("criteria.id"), nullable=False, index=True, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"), nullable=False, index=True, primary_key=True)
    score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    def to_dict(self) -> ApplicantScoreSchema:
        return ApplicantScoreSchema(
            criteria_id=self.criteria_id,
            applicant_id=self.applicant_id,
            score=self.score,
            created_at=self.created_at,
        )
