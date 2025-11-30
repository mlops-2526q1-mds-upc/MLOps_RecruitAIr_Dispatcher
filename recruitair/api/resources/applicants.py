from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from ...database.models import Applicant, JobOffer
from .. import SessionDep, app


class CreateApplicantRequest(BaseModel):
    cv: str = Field(
        ...,
        description="Curriculum vitae of the applicant",
        examples=["Experienced software engineer with a background in AI."],
    )


@app.post("/job_offers/{offer_id}/applicants", tags=["Applicants"])
def create_applicant(offer_id: int, request: CreateApplicantRequest, db: SessionDep):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    new_applicant = Applicant(cv=request.cv, offer_id=offer_id)
    db.add(new_applicant)
    db.commit()
    return {"message": "Created successfully", "applicant": new_applicant}


@app.get("/job_offers/{offer_id}/applicants", tags=["Applicants"])
def get_applicant(offer_id: int, db: SessionDep, limit: int = 100, offset: int = 0, cv: Optional[str] = None):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    query = db.query(Applicant).filter(Applicant.offer_id == offer_id)
    if cv:
        query = query.filter(Applicant.cv.contains(cv))
    results = query.order_by(Applicant.id).offset(offset).limit(limit).all()
    return {"applicants": results}
