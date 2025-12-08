import time
from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from ...database.models import JobOffer, JobOfferSchema, JobOfferStatus
from .. import SessionDep, app
from ..monitoring.job_offers import (
    CREATE_OFFER_REQUESTS,
    CREATE_OFFER_REQUESTS_ERRORS,
    CREATE_OFFER_REQUESTS_TIME,
    CREATE_OFFER_TEXT_LENGTH,
    CREATED_OFFERS,
    GET_OFFER_REQUESTS,
    GET_OFFER_REQUESTS_ERRORS,
    GET_OFFER_REQUESTS_TIME,
    LIST_OFFERS_REQUESTS,
    LIST_OFFERS_REQUESTS_ERRORS,
    LIST_OFFERS_REQUESTS_TIME,
    LIST_OFFERS_RETURNED_PER_REQUEST,
)


class CreateJobOfferRequest(BaseModel):
    text: str = Field(
        ...,
        description="Text description of the job offer",
        examples=["Looking for a software engineer with experience in Python and FastAPI."],
    )


class CreateJobOfferResponse(BaseModel):
    message: str = Field(..., description="Response message", examples=["Created successfully"])
    job_offer: JobOfferSchema = Field(..., description="Details of the created job offer")


@app.post("/job_offers", tags=["Job Offers"])
def create_job_offer(request: CreateJobOfferRequest, db: SessionDep) -> CreateJobOfferResponse:
    CREATE_OFFER_REQUESTS.inc()
    time_start = time.monotonic()
    try:
        new_offer = JobOffer(text=request.text)
        db.add(new_offer)
        db.commit()
        db.refresh(new_offer)
    except Exception as e:
        CREATE_OFFER_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        CREATE_OFFER_REQUESTS_TIME.observe(elapsed_time)
    CREATE_OFFER_TEXT_LENGTH.observe(len(request.text))
    CREATED_OFFERS.inc()
    return CreateJobOfferResponse(message="Created successfully", job_offer=new_offer.to_dict())


class ListJobOffersResponse(BaseModel):
    job_offers: List[JobOfferSchema] = Field(..., description="List of job offers")
    cursor: int = Field(..., description="Cursor for pagination")


@app.get("/job_offers", tags=["Job Offers"])
def list_job_offers(
    db: SessionDep,
    limit: int = 100,
    offset: int = 0,
    text: Optional[str] = None,
    status: Optional[JobOfferStatus] = None,
) -> ListJobOffersResponse:
    LIST_OFFERS_REQUESTS.inc()
    time_start = time.monotonic()
    try:
        query = db.query(JobOffer)
        if text:
            query = query.filter(JobOffer.text.contains(text))
        if status:
            query = query.filter(JobOffer.status == status)

        results = query.order_by(JobOffer.id).offset(offset).limit(limit).all()
        cursor = offset + len(results)
    except Exception as e:
        LIST_OFFERS_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        LIST_OFFERS_REQUESTS_TIME.observe(elapsed_time)
    LIST_OFFERS_RETURNED_PER_REQUEST.observe(len(results))
    return ListJobOffersResponse(job_offers=[offer.to_dict() for offer in results], cursor=cursor)


class GetJobOfferResponse(BaseModel):
    job_offer: JobOfferSchema = Field(..., description="Details of the job offer")


@app.get("/job_offers/{offer_id}", tags=["Job Offers"])
def get_job_offer(offer_id: int, db: SessionDep) -> GetJobOfferResponse:
    GET_OFFER_REQUESTS.inc()
    time_start = time.monotonic()
    try:
        offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
    except Exception as e:
        GET_OFFER_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        GET_OFFER_REQUESTS_TIME.observe(elapsed_time)
    return GetJobOfferResponse(job_offer=offer.to_dict())
