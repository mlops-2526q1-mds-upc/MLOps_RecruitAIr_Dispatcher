from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from ...database.models import Applicant, ApplicantSchema, JobOffer
from .. import SessionDep, app


class CreateApplicantRequest(BaseModel):
    cv: str = Field(
        ...,
        description="Curriculum vitae of the applicant",
        examples=["Experienced software engineer with a background in AI."],
    )


class CreateApplicantResponse(BaseModel):
    message: str = Field(..., description="Response message", examples=["Created successfully"])
    applicants: List[ApplicantSchema] = Field(..., description="List of created applicants")


@app.post("/job_offers/{offer_id}/applicants", tags=["Applicants"])
def create_applicant(offer_id: int, request: List[CreateApplicantRequest], db: SessionDep) -> CreateApplicantResponse:
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    created_applicants: List[Applicant] = []
    for item in request:
        new_applicant = Applicant(cv=item.cv, offer_id=offer_id)
        db.add(new_applicant)
        created_applicants.append(new_applicant)
    db.commit()
    for applicant in created_applicants:
        db.refresh(applicant)
    return CreateApplicantResponse(
        message="Created successfully", applicants=[applicant.to_dict() for applicant in created_applicants]
    )


class GetApplicantsResponse(BaseModel):
    applicants: List[ApplicantSchema] = Field(..., description="List of applicants for the job offer")


@app.get("/job_offers/{offer_id}/applicants", tags=["Applicants"])
def get_applicant(
    offer_id: int, db: SessionDep, limit: int = 100, offset: int = 0, cv: Optional[str] = None
) -> GetApplicantsResponse:
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    query = db.query(Applicant).filter(Applicant.offer_id == offer_id)
    if cv:
        query = query.filter(Applicant.cv.contains(cv))
    results = query.order_by(Applicant.id).offset(offset).limit(limit).all()
    return GetApplicantsResponse(applicants=[applicant.to_dict() for applicant in results])
