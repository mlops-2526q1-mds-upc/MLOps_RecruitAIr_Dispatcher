import time
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field

from recruitair.database.models.applicant_score import ApplicantScore

from ...database.models import Criterion, CriterionSchema, JobOffer
from .. import SessionDep, app
from ..monitoring.criteria import (
    CREATE_CRITERIA_DESCRIPTION_LENGTH,
    CREATE_CRITERIA_IMPORTANCE,
    CREATE_CRITERIA_REQUESTS,
    CREATE_CRITERIA_REQUESTS_ERRORS,
    CREATE_CRITERIA_REQUESTS_TIME,
    CRITERIA_CREATED,
    CRITERIA_CREATED_PER_REQUEST,
    GET_CRITERIA_REQUESTS,
    GET_CRITERIA_REQUESTS_ERRORS,
    GET_CRITERIA_REQUESTS_TIME,
    GET_CRITERIA_RETURNED_PER_REQUEST,
    UPDATE_CRITERION_DESCRIPTION_LENGTH,
    UPDATE_CRITERION_IMPORTANCE,
    UPDATE_CRITERION_REQUESTS,
    UPDATE_CRITERION_REQUESTS_ERRORS,
    UPDATE_CRITERION_REQUESTS_TIME,
)


class CriteriaItem(BaseModel):
    description: str = Field(..., description="Description of the extracted criterion from the job offer")
    importance: float = Field(
        ..., description="Importance of the extracted criterion on a scale from 0 to 1", ge=0, le=1
    )


class GetJobOfferCriteriaResponse(BaseModel):
    criteria: List[CriterionSchema] = Field(..., description="List of criteria for the job offer")


@app.get("/job_offers/{offer_id}/criteria", tags=["Criteria"])
def get_job_offer_criteria(offer_id: int, db: SessionDep) -> GetJobOfferCriteriaResponse:
    GET_CRITERIA_REQUESTS.inc()
    time_start = time.monotonic()
    try:
        offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        criteria = db.query(Criterion).filter(Criterion.offer_id == offer_id).all()
    except Exception as e:
        GET_CRITERIA_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        GET_CRITERIA_REQUESTS_TIME.observe(elapsed_time)
    GET_CRITERIA_RETURNED_PER_REQUEST.observe(len(criteria))
    return GetJobOfferCriteriaResponse(criteria=[criterion.to_dict() for criterion in criteria])


class AddJobOfferCriteriaRequest(BaseModel):
    criteria: List[CriteriaItem] = Field(..., description="List of criteria to be added to the job offer")


class AddJobOfferCriteriaResponse(BaseModel):
    message: str = Field(..., description="Response message", examples=["Criteria added successfully"])
    criteria: List[CriterionSchema] = Field(..., description="List of added criteria")


@app.post("/job_offers/{offer_id}/criteria", tags=["Criteria"])
def add_job_offer_criteria(
    offer_id: int, request: AddJobOfferCriteriaRequest, db: SessionDep
) -> AddJobOfferCriteriaResponse:
    CREATE_CRITERIA_REQUESTS.inc()
    time_start = time.monotonic()
    try:
        offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        created_criteria: List[Criterion] = []
        for item in request.criteria:
            CREATE_CRITERIA_DESCRIPTION_LENGTH.observe(len(item.description))
            CREATE_CRITERIA_IMPORTANCE.observe(item.importance)
            new_criterion = Criterion(offer_id=offer_id, description=item.description, importance=item.importance)
            db.add(new_criterion)
            created_criteria.append(new_criterion)
        db.commit()
        for criterion in created_criteria:
            db.refresh(criterion)
    except Exception as e:
        CREATE_CRITERIA_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        CREATE_CRITERIA_REQUESTS_TIME.observe(elapsed_time)
    CRITERIA_CREATED.inc(len(created_criteria))
    CRITERIA_CREATED_PER_REQUEST.observe(len(created_criteria))
    return AddJobOfferCriteriaResponse(
        message="Criteria added successfully", criteria=[criterion.to_dict() for criterion in created_criteria]
    )


class UpdateCriterionRequest(BaseModel):
    description: Optional[str] = Field(None, description="Updated description of the criterion")
    importance: Optional[float] = Field(
        None, description="Updated importance of the criterion on a scale from 0 to 1", ge=0, le=1
    )


class UpdateCriterionResponse(BaseModel):
    message: str = Field(..., description="Response message", examples=["Updated successfully"])
    criterion: CriterionSchema = Field(..., description="Details of the updated criterion")


@app.put("/job_offers/{offer_id}/criteria/{criterion_id}", tags=["Criteria"])
def update_criterion(
    offer_id: int, criterion_id: int, request: UpdateCriterionRequest, db: SessionDep
) -> UpdateCriterionResponse:
    UPDATE_CRITERION_REQUESTS.inc()
    time_start = time.monotonic()
    try:
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
    except Exception as e:
        UPDATE_CRITERION_REQUESTS_ERRORS.inc()
        raise e
    finally:
        elapsed_time = time.monotonic() - time_start
        UPDATE_CRITERION_REQUESTS_TIME.observe(elapsed_time)
    if request.description is not None:
        UPDATE_CRITERION_DESCRIPTION_LENGTH.observe(len(request.description))
    if request.importance is not None:
        UPDATE_CRITERION_IMPORTANCE.observe(request.importance)
    return UpdateCriterionResponse(message="Updated successfully", criterion=criterion.to_dict())
