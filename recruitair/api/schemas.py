from pydantic import BaseModel
from enum import Enum
from typing import Optional, Dict, Any

class JobOfferStatus(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"

class JobOfferCreate(BaseModel):
    text: str

class JobOfferUpdate(BaseModel):
    criteria: Optional[str] = None

class JobOfferGet(BaseModel):
    text: Optional[str] = None
    criteria: Optional[str] = None
    status: Optional[JobOfferStatus] = None

class ApplicantCreate(BaseModel):
    cv: Dict[str, Any]

class ApplicantUpdate(BaseModel):
    scores: Dict[str, Any]

class ApplicantGet(BaseModel):
    cv: Optional[Dict[str, Any]] = None
    scores: Optional[Dict[str, Any]] = None
