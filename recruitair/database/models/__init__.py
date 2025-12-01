# Job Offer
# Criterion
# Applicant
# Applicant Score


from sqlalchemy.orm import declarative_base, registry

Base = declarative_base()
mapper_registry = registry()


from .applicant import Applicant, ApplicantSchema
from .applicant_score import ApplicantScore, ApplicantScoreSchema
from .criterion import Criterion, CriterionSchema
from .job_offer import JobOffer, JobOfferSchema, JobOfferStatus

__all__ = ["Applicant", "ApplicantScore", "Criterion", "JobOffer", "JobOfferStatus"]
