from .database import get_session
from .database.models import Applicant, ApplicantScore, Criterion, JobOffer


def test_database():
    with get_session() as session:
        # Test JobOffer creation
        job_offer = JobOffer(text="Test Job Offer")
        session.add(job_offer)
        session.commit()
        assert job_offer.id is not None

        # Test Criterion creation
        criterion = Criterion(offer_id=job_offer.id, description="Test Criterion", importance=1.0)
        session.add(criterion)
        session.commit()
        assert criterion.id is not None

        # Test Applicant creation
        applicant = Applicant(cv="Test CV", offer_id=job_offer.id)
        session.add(applicant)
        session.commit()
        assert applicant.id is not None

        # Test ApplicantScore creation
        applicant_score = ApplicantScore(criteria_id=criterion.id, applicant_id=applicant.id, score=95.0)
        session.add(applicant_score)
        session.commit()
        assert applicant_score.criteria_id == criterion.id
        assert applicant_score.applicant_id == applicant.id


if __name__ == "__main__":
    test_database()
