from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


class ApplicantScore(Base):
    __tablename__ = "applicant_scores"

    criteria_id = Column(Integer, ForeignKey("criteria.id"), nullable=False, index=True, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"), nullable=False, index=True, primary_key=True)
    score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
