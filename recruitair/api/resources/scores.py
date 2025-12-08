import time
from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ...database.models import (
    Applicant,
    ApplicantScore,
    ApplicantScoreSchema,
    Criterion,
    JobOffer,
)
from .. import SessionDep, app
from ..monitoring.scores import (
    GET_SCORE_REQUESTS,
    GET_SCORE_REQUESTS_ERRORS,
    GET_SCORE_REQUESTS_TIME,
    GET_SCORES_REQUESTS,
    GET_SCORES_REQUESTS_ERRORS,
    GET_SCORES_REQUESTS_TIME,
    GET_SCORES_RETURNED_PER_REQUEST,
    SCORE_VALUES,
    UPDATE_SCORE_REQUESTS,
    UPDATE_SCORE_REQUESTS_ERRORS,
    UPDATE_SCORE_REQUESTS_TIME,
    UPDATE_SCORE_VALUE_DIFFERENCE,
)


class GetApplicantScoresResponse(BaseModel):
    scores: List[ApplicantScoreSchema] = Field(..., description="List of scores for the applicant")


@app.get("/job_offers/{offer_id}/applicants/{applicant_id}/scores", tags=["Scores"])
def get_applicant_scores(offer_id: int, applicant_id: int, db: SessionDep) -> GetApplicantScoresResponse:
    GET_SCORES_REQUESTS.inc()
    time_start = time.monotonic()
    try:
        offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")

        applicant = db.query(Applicant).filter(Applicant.id == applicant_id, Applicant.offer_id == offer_id).first()

        if not applicant:
            raise HTTPException(status_code=404, detail="Applicant not found")

        scores = db.query(ApplicantScore).filter(ApplicantScore.applicant_id == applicant_id).all()
        if not scores:
            raise HTTPException(status_code=404, detail="Scores not found for the applicant")
        for score in scores:
            SCORE_VALUES.observe(float(score.score))
    except Exception as e:
        GET_SCORES_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        GET_SCORES_REQUESTS_TIME.observe(elapsed_time)
    GET_SCORES_RETURNED_PER_REQUEST.observe(len(scores))

    return GetApplicantScoresResponse(scores=[score.to_dict() for score in scores])


class GetApplicantScoreResponse(BaseModel):
    score: ApplicantScoreSchema = Field(..., description="Score of the applicant for the given criterion")


@app.get("/job_offers/{offer_id}/applicants/{applicant_id}/scores/{criterion_id}", tags=["Scores"])
def get_applicant_score(
    offer_id: int, applicant_id: int, criterion_id: int, db: SessionDep
) -> GetApplicantScoreResponse:
    GET_SCORE_REQUESTS.inc()
    time_start = time.monotonic()
    try:
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
        SCORE_VALUES.observe(float(score.score))
    except Exception as e:
        GET_SCORE_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        GET_SCORE_REQUESTS_TIME.observe(elapsed_time)

    return GetApplicantScoreResponse(score=score.to_dict())


class UpdateApplicantScoreRequest(BaseModel):
    score: float = Field(..., description="Score value for the applicant on the given criterion")


class UpdateApplicantScoreResponse(BaseModel):
    score: ApplicantScoreSchema = Field(..., description="Updated score of the applicant for the given criterion")


@app.put("/job_offers/{offer_id}/applicants/{applicant_id}/scores/{criterion_id}", tags=["Scores"])
def update_applicant_score(
    offer_id: int, applicant_id: int, criterion_id: int, request: UpdateApplicantScoreRequest, db: SessionDep
) -> UpdateApplicantScoreResponse:
    UPDATE_SCORE_REQUESTS.inc()
    time_start = time.monotonic()
    try:
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
        UPDATE_SCORE_VALUE_DIFFERENCE.observe(request.score - float(score.score))
    except Exception as e:
        UPDATE_SCORE_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        UPDATE_SCORE_REQUESTS_TIME.observe(elapsed_time)

    return UpdateApplicantScoreResponse(score=score.to_dict())
