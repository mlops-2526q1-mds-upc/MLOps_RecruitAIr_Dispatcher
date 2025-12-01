from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import text as sql_text
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


class JobOfferStatus(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"


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


class JobOffer(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(JobOfferStatus), nullable=False, index=True, default=JobOfferStatus.PENDING)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=sql_text("CURRENT_TIMESTAMP"))

    def to_dict(self) -> JobOfferSchema:
        return JobOfferSchema(
            id=self.id,
            text=self.text,
            status=self.status,
            created_at=self.created_at,
        )
