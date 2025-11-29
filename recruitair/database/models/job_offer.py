from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import text as sql_text
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


class JobOfferStatus(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"


class JobOffer(Base):
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(JobOfferStatus), nullable=False, index=True, default=JobOfferStatus.PENDING)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=sql_text("CURRENT_TIMESTAMP"))
