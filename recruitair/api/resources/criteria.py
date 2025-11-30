from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from recruitair.database.models.applicant_score import ApplicantScore

from ...database.models import Criterion, JobOffer
from .. import SessionDep, app


class CriteriaItem(BaseModel):
    description: str = Field(..., description="Description of the extracted criterion from the job offer")
    importance: float = Field(
        ..., description="Importance of the extracted criterion on a scale from 0 to 1", ge=0, le=1
    )


@app.get("/job_offers/{offer_id}/criteria", tags=["Criteria"])
def get_job_offer_criteria(offer_id: int, db: SessionDep):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    criteria = db.query(Criterion).filter(Criterion.offer_id == offer_id).all()
    return {"criteria": criteria}


@app.post("/job_offers/{offer_id}/criteria", tags=["Criteria"])
def add_job_offer_criteria(offer_id: int, request: List[CriteriaItem], db: SessionDep):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    created_criteria: List[Criterion] = []
    for item in request:
        new_criterion = Criterion(offer_id=offer_id, description=item.description, importance=item.importance)
        db.add(new_criterion)
        created_criteria.append(new_criterion)
    db.commit()
    return {"message": "Criteria added successfully", "criteria": created_criteria}


class UpdateCriterionRequest(BaseModel):
    description: Optional[str] = Field(None, description="Updated description of the criterion")
    importance: Optional[float] = Field(
        None, description="Updated importance of the criterion on a scale from 0 to 1", ge=0, le=1
    )


@app.put("/job_offers/{offer_id}/criteria/{criterion_id}", tags=["Criteria"])
def update_criterion(offer_id: int, criterion_id: int, request: UpdateCriterionRequest, db: SessionDep):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    criterion = db.query(Criterion).filter(Criterion.id == criterion_id, Criterion.offer_id == offer_id).first()
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")

    if request.description is not None:
        criterion.description = request.description
        # In this case, remove all associated scores since the criterion has changed
        db.query(ApplicantScore).filter(ApplicantScore.criteria_id == criterion_id).delete()
    if request.importance is not None:
        criterion.importance = request.importance
    db.commit()
    db.refresh(criterion)
    return {"message": "Updated successfully", "criterion": criterion}
