from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from recruitair.api.database import get_db
from recruitair.api.schemas import JobOfferCreate, JobOfferGet, JobOfferUpdate, ApplicantCreate, ApplicantUpdate, ApplicantGet
from recruitair.database.models.job_offer import JobOffer
from recruitair.database.models.applicant import Applicant
from recruitair.database.models.applicant_score import ApplicantScore
from recruitair.database.models.criterion import Criterion

app = FastAPI(title="RecruitAIr API", version="1.0.0")


# -----------------------
# JOB OFFER ENDPOINTS
# -----------------------

@app.post("/job_offers")
def create_job_offer(request: JobOfferCreate, db: Session = Depends(get_db)):
    new_offer = JobOffer(text=request.text)
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return {"message": "Created successfully", "job_offer": new_offer}


@app.get("/job_offers")
def get_job_offer(request: JobOfferGet = Depends(), db: Session = Depends(get_db)):
    query = db.query(JobOffer)
    if request.text:
        query = query.filter(JobOffer.text.contains(request.text))
    if request.criteria:
        query = query.filter(JobOffer.text.contains(request.criteria))
    if request.status:
        query = query.filter(JobOffer.status == request.status)
    results = query.all()
    return {"job_offers": results}


@app.put("/job_offers/{offer_id}")
def update_job_offer(offer_id: int, request: JobOfferUpdate, db: Session = Depends(get_db)):
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    if request.criteria:
        offer.text += f" | Updated with criteria: {request.criteria}"
    db.commit()
    return {"message": "Updated successfully", "job_offer": offer}


# -----------------------
# APPLICANT ENDPOINTS
# -----------------------

@app.post("/applicants")
def create_applicant(request: ApplicantCreate, db: Session = Depends(get_db)):
    new_applicant = Applicant(cv=request.cv)
    db.add(new_applicant)
    db.commit()
    db.refresh(new_applicant)
    return {"message": "Created successfully", "applicant": new_applicant}


@app.get("/applicants")
def get_applicant(request: ApplicantGet = Depends(), db: Session = Depends(get_db)):
    query = db.query(Applicant)
    if request.cv:
        query = query.filter(Applicant.cv.contains(request.cv))
    results = query.all()
    return {"applicants": results}


@app.put("/applicants/{applicant_id}")
def update_applicant(applicant_id: int, request: ApplicantUpdate, db: Session = Depends(get_db)):
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()

    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    # Update scores (stored in ApplicantScore)
    score = db.query(ApplicantScore).filter(ApplicantScore.applicant_id == applicant_id).first()
    if not score:
        score = ApplicantScore(applicant_id=applicant_id, scores=request.scores)
        db.add(score)
    else:
        score.scores = request.scores

    db.commit()
    db.refresh(applicant)
    return {"message": "Updated successfully", "applicant": applicant}
