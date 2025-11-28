from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from sqlalchemy import TIMESTAMP, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


class Criterion(Base):
    __tablename__ = "criteria"

    id: int = Column(Integer, primary_key=True, index=True)
    offer_id: int = Column(Integer, ForeignKey("job_offers.id"), nullable=False, index=True)
    description: str = Column(String, nullable=False)
    importance: float = Column(Float, nullable=False)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
