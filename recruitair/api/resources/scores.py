from enum import Enum
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ...database.models import Applicant, ApplicantScore, Criterion, JobOffer
from .. import SessionDep, app


@app.get("/job_offers/{offer_id}/applicants/{applicant_id}/scores", tags=["Scores"])
def get_applicant_scores(offer_id: int, applicant_id: int, db: SessionDep):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    applicant = db.query(Applicant).filter(Applicant.id == applicant_id, Applicant.offer_id == offer_id).first()

    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    scores = db.query(ApplicantScore).filter(ApplicantScore.applicant_id == applicant_id).all()
    if not scores:
        raise HTTPException(status_code=404, detail="Scores not found for the applicant")

    return {"scores": scores}


@app.get("/job_offers/{offer_id}/applicants/{applicant_id}/scores/{criterion_id}", tags=["Scores"])
def get_applicant_score(offer_id: int, applicant_id: int, criterion_id: int, db: SessionDep):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    applicant = db.query(Applicant).filter(Applicant.id == applicant_id, Applicant.offer_id == offer_id).first()

    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    criterion = db.query(Criterion).filter(Criterion.id == criterion_id, Criterion.offer_id == offer_id).first()
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")

    score = (
        db.query(ApplicantScore)
        .filter(ApplicantScore.applicant_id == applicant_id, ApplicantScore.criteria_id == criterion_id)
        .first()
    )
    if not score:
        raise HTTPException(status_code=404, detail="Score has not been computed yet")

    return {"score": score}


class UpdateApplicantScoreRequest(BaseModel):
    score: float = Field(..., description="Score value for the applicant on the given criterion")


@app.put("/job_offers/{offer_id}/applicants/{applicant_id}/scores/{criterion_id}", tags=["Scores"])
def update_applicant_score(
    offer_id: int, applicant_id: int, criterion_id: int, request: UpdateApplicantScoreRequest, db: SessionDep
):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")

    applicant = db.query(Applicant).filter(Applicant.id == applicant_id, Applicant.offer_id == offer_id).first()

    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    criterion = db.query(Criterion).filter(Criterion.id == criterion_id, Criterion.offer_id == offer_id).first()
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found")

    score = (
        db.query(ApplicantScore)
        .filter(ApplicantScore.applicant_id == applicant_id, ApplicantScore.criteria_id == criterion_id)
        .first()
    )
    if not score:
        raise HTTPException(status_code=404, detail="Score has not been computed yet")

    score.score = request.score
    db.commit()
    db.refresh(score)

    return {"score": score}
