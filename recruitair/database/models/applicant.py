from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import text as sql_text

from . import Base


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


class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    cv = Column(String, nullable=False)
    offer_id = Column(Integer, ForeignKey("job_offers.id"), nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=sql_text("CURRENT_TIMESTAMP"))

    def to_dict(self) -> ApplicantSchema:
        return ApplicantSchema(
            id=self.id,
            cv=self.cv,
            offer_id=self.offer_id,
            created_at=self.created_at,
        )
