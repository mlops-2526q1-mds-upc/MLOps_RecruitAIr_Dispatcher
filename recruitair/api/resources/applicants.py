import time
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from ...database.models import Applicant, ApplicantSchema, JobOffer
from .. import SessionDep, app
from ..monitoring.applicants import (
    APPLICANT_CV_LENGTH,
    APPLICANTS_CREATED,
    APPLICANTS_CREATED_PER_REQUEST,
    APPLICANTS_RETURNED_PER_REQUEST,
    CREATE_APPLICANTS_REQUESTS,
    CREATE_APPLICANTS_REQUESTS_ERRORS,
    CREATE_APPLICANTS_REQUESTS_TIME,
    GET_APPLICANTS_REQUESTS,
    GET_APPLICANTS_REQUESTS_ERRORS,
    GET_APPLICANTS_REQUESTS_TIME,
)


class CreateApplicantsRequest(BaseModel):
    class ApplicantItem(BaseModel):
        cv: str = Field(
            ...,
            description="Curriculum vitae of the applicant",
            examples=["Experienced software engineer with a background in AI."],
        )

    applicants: List[ApplicantItem] = Field(..., description="List of applicants to be created")


class CreateApplicantsResponse(BaseModel):
    message: str = Field(..., description="Response message", examples=["Created successfully"])
    applicants: List[ApplicantSchema] = Field(..., description="List of created applicants")


@app.post("/job_offers/{offer_id}/applicants", tags=["Applicants"])
def create_applicants(offer_id: int, request: CreateApplicantsRequest, db: SessionDep) -> CreateApplicantsResponse:
    CREATE_APPLICANTS_REQUESTS.inc()
    time_start = time.monotonic()
    try:
        offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")

        created_applicants: List[Applicant] = []
        for item in request.applicants:
            APPLICANT_CV_LENGTH.observe(len(item.cv))
            new_applicant = Applicant(cv=item.cv, offer_id=offer_id)
            db.add(new_applicant)
            created_applicants.append(new_applicant)
        db.commit()
        for applicant in created_applicants:
            db.refresh(applicant)
    except Exception as e:
        CREATE_APPLICANTS_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        CREATE_APPLICANTS_REQUESTS_TIME.observe(elapsed_time)
    APPLICANTS_CREATED.inc(len(created_applicants))
    APPLICANTS_CREATED_PER_REQUEST.observe(len(created_applicants))
    return CreateApplicantsResponse(
        message="Created successfully", applicants=[applicant.to_dict() for applicant in created_applicants]
    )


class GetApplicantsResponse(BaseModel):
    applicants: List[ApplicantSchema] = Field(..., description="List of applicants for the job offer")


@app.get("/job_offers/{offer_id}/applicants", tags=["Applicants"])
def get_applicants(
    offer_id: int, db: SessionDep, limit: int = 100, offset: int = 0, cv: Optional[str] = None
) -> GetApplicantsResponse:
    GET_APPLICANTS_REQUESTS.inc()
    time_start = time.monotonic()
    try:
        offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")

        query = db.query(Applicant).filter(Applicant.offer_id == offer_id)
        if cv:
            query = query.filter(Applicant.cv.contains(cv))
        results = query.order_by(Applicant.id).offset(offset).limit(limit).all()
    except Exception as e:
        GET_APPLICANTS_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        GET_APPLICANTS_REQUESTS_TIME.observe(elapsed_time)
    APPLICANTS_RETURNED_PER_REQUEST.observe(len(results))
    return GetApplicantsResponse(applicants=[applicant.to_dict() for applicant in results])
