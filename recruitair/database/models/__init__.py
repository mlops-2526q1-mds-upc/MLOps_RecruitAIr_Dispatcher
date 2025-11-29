# Job Offer
# Criterion
# Applicant
# Applicant Score


from sqlalchemy.orm import declarative_base, registry

Base = declarative_base()
mapper_registry = registry()


from .applicant import Applicant
from .applicant_score import ApplicantScore
from .criterion import Criterion
from .job_offer import JobOffer, JobOfferStatus

__all__ = ["Applicant", "ApplicantScore", "Criterion", "JobOffer", "JobOfferStatus"]
