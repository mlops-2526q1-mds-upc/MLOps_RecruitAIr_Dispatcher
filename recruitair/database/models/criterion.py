from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


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


class Criterion(Base):
    __tablename__ = "criteria"

    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("job_offers.id"), nullable=False, index=True)
    description = Column(String, nullable=False)
    importance = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    def to_dict(self) -> CriterionSchema:
        return CriterionSchema(
            id=self.id,
            description=self.description,
            importance=self.importance,
            offer_id=self.offer_id,
        )
