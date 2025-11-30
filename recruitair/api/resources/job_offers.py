from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from ...database.models import JobOffer
from .. import SessionDep, app


class JobOfferStatus(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"


class CreateJobOfferRequest(BaseModel):
    text: str = Field(
        ...,
        description="Text description of the job offer",
        examples=["Looking for a software engineer with experience in Python and FastAPI."],
    )


@app.post("/job_offers", tags=["Job Offers"])
def create_job_offer(request: CreateJobOfferRequest, db: SessionDep):
    new_offer = JobOffer(text=request.text)
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return {"message": "Created successfully", "job_offer": new_offer}


@app.get("/job_offers", tags=["Job Offers"])
def list_job_offers(
    db: SessionDep,
    limit: int = 100,
    offset: int = 0,
    text: Optional[str] = None,
    status: Optional[JobOfferStatus] = None,
):
    query = db.query(JobOffer)
    if text:
        query = query.filter(JobOffer.text.contains(text))
    if status:
        query = query.filter(JobOffer.status == status)

    results = query.order_by(JobOffer.id).offset(offset).limit(limit).all()
    cursor = offset + len(results)
    return {"job_offers": results, "cursor": cursor}


@app.get("/job_offers/{offer_id}", tags=["Job Offers"])
def get_job_offer(offer_id: int, db: SessionDep):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return {"job_offer": offer}
