import json
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Test comment
import urllib.request

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

JOB_POSTINGS_DEMO_DATASET = "https://datasets-server.huggingface.co/rows?dataset=datastax%2Flinkedin_job_listings&config=default&split=train&offset=0&length=100"
CVS_DEMO_DATASET = "https://datasets-server.huggingface.co/rows?dataset=lang-uk%2Frecruitment-dataset-candidate-profiles-english&config=default&split=train&offset=0&length=100"


def create_examples(
    get_session: sessionmaker,
    add_offers: bool = False,
    add_applicants: bool = False,
    add_criteria: bool = False,
    add_scores: bool = False,
) -> None:

    with get_session() as session:
        if add_offers:
            postings_dataset = urllib.request.urlopen(JOB_POSTINGS_DEMO_DATASET)
            data = json.load(postings_dataset)
            job_texts = [item["row"]["description"] for item in data["rows"]]

            for job_text in job_texts:
                session.execute(
                    text(
                        """
                    INSERT INTO job_offers (text, status)
                    VALUES (:text, 'PENDING')
                    """
                    ),
                    {"text": job_text},
                )
            session.commit()
            total_offers = session.execute(text("SELECT COUNT(*) FROM job_offers")).scalar()
            print(f"Inserted {len(job_texts)} job offers into the database.")
            print(f"There are now {total_offers} job offers in the database.")

        if add_applicants:
            cvs_dataset = urllib.request.urlopen(CVS_DEMO_DATASET)
            data = json.load(cvs_dataset)
            cvs = [item["row"]["CV"] for item in data["rows"]]
            jobs = session.execute(text("SELECT id, text FROM job_offers")).fetchall()
            inserted_applicants = 0
            for job in jobs:
                # For each job offer, create random applicants
                num_applicants = random.randint(5, 30)
                random.shuffle(cvs)
                for cv_text in cvs[:num_applicants]:
                    session.execute(
                        text(
                            """
                        INSERT INTO applicants (offer_id, cv)
                        VALUES (:offer_id, :cv)
                        """
                        ),
                        {"offer_id": job.id, "cv": cv_text},
                    )
                    inserted_applicants += 1
            session.commit()
            total_applicants = session.execute(text("SELECT COUNT(*) FROM applicants")).scalar()
            print(f"Inserted {inserted_applicants} applicants into the database.")
            print(f"There are now {total_applicants} applicants in the database.")

        if add_criteria:
            jobs = session.execute(text("SELECT id, text FROM job_offers")).fetchall()
            inserted_criteria = 0
            for job in jobs:
                num_criteria = random.randint(3, 10)
                for i in range(num_criteria):
                    session.execute(
                        text(
                            """
                        INSERT INTO criteria (offer_id, description, importance)
                        VALUES (:offer_id, :description, :importance)
                        """
                        ),
                        {
                            "offer_id": job.id,
                            "description": f"Criterion {i+1} for job {job.id}",
                            "importance": round(random.uniform(0.1, 1.0), 2),
                        },
                    )
                    inserted_criteria += 1
            session.commit()
            total_criteria = session.execute(text("SELECT COUNT(*) FROM criteria")).scalar()
            print(f"Inserted {inserted_criteria} criteria into the database.")
            print(f"There are now {total_criteria} criteria in the database.")

        if add_scores:
            criteria = session.execute(text("SELECT id, offer_id FROM criteria")).fetchall()
            inserted_scores = 0
            for criterion in criteria:
                applicants = session.execute(
                    text("SELECT id FROM applicants WHERE offer_id = :offer_id"),
                    {"offer_id": criterion.offer_id},
                ).fetchall()
                for applicant in applicants:
                    score_value = round(random.uniform(0.0, 1.0), 2)
                    session.execute(
                        text(
                            """
                        INSERT INTO applicant_scores (applicant_id, criteria_id, score)
                        VALUES (:applicant_id, :criteria_id, :score)
                        """
                        ),
                        {
                            "applicant_id": applicant.id,
                            "criteria_id": criterion.id,
                            "score": score_value,
                        },
                    )
                    inserted_scores += 1
            session.commit()
            total_scores = session.execute(text("SELECT COUNT(*) FROM applicant_scores")).scalar()
            print(f"Inserted {inserted_scores} scores into the database.")
            print(f"There are now {total_scores} scores in the database.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create example job offers and applicants in the database.")
    parser.add_argument("database_url", type=str, help="Database URL for connecting to the database.")
    parser.add_argument("--add-offers", action="store_true", help="Add job offers to the database.")
    parser.add_argument("--add-applicants", action="store_true", help="Add applicants to the database.")
    parser.add_argument("--add-criteria", action="store_true", help="Add criteria to the job offers.")
    parser.add_argument("--add-scores", action="store_true", help="Add scores to the applicants.")
    args = parser.parse_args()

    engine = create_engine(args.database_url)
    SessionLocal = sessionmaker(bind=engine)

    create_examples(
        get_session=SessionLocal,
        add_criteria=args.add_criteria,
        add_scores=args.add_scores,
        add_offers=args.add_offers,
        add_applicants=args.add_applicants,
    )
