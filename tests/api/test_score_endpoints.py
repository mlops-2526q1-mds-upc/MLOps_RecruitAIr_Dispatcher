from fastapi.testclient import TestClient

# ------------- SCORE TESTS ------------- #


def test_get_score_for_applicant(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Data Scientist"})
    offer_id = response.json()["job_offer"]["id"]

    # Create criteria for the job offer
    criteria = [
        {"description": "Experience in data science", "importance": 0.6},
        {"description": "Proficiency in Python", "importance": 0.4},
    ]
    response = client.post(f"/job_offers/{offer_id}/criteria", json={"criteria": criteria})
    criteria = response.json()["criteria"]

    # Create an applicant for the job offer
    cv_text = "Name: Alice Smith\nExperience: 4 years in data science\nSkills: Python, R, SQL"
    response = client.post(f"/job_offers/{offer_id}/applicants", json={"applicants": [{"cv": cv_text}]})
    applicant_id = response.json()["applicants"][0]["id"]

    # Create the scores directly in the database (there's no endpoint for this)
    from recruitair.api import app
    from recruitair.database import get_db_session
    from recruitair.database.models import ApplicantScore

    # Get the get_db dependency
    # This is a workaround to access the database session
    db_dependency = app.dependency_overrides.get(get_db_session)
    score_values = [8.0, 9.0]  # Example scores for the criteria
    db = next(db_dependency())
    scores = []
    for criterion, score_value in zip(criteria, score_values):
        score = ApplicantScore(
            criteria_id=criterion["id"],
            applicant_id=applicant_id,
            score=score_value,
        )
        scores.append(score)
    db.add_all(scores)
    db.commit()
    db.close()

    # Retrieve score for the applicant
    response = client.get(f"/job_offers/{offer_id}/applicants/{applicant_id}/scores")
    assert response.status_code == 200
    data = response.json()
    assert "scores" in data
    assert len(data["scores"]) == 2
    for score_entry, criterion, expected_score in zip(data["scores"], criteria, score_values):
        assert "score" in score_entry
        assert score_entry["score"] == expected_score
        assert "applicant_id" in score_entry
        assert score_entry["applicant_id"] == applicant_id
        assert "criteria_id" in score_entry
        assert score_entry["criteria_id"] == criterion["id"]
        assert "created_at" in score_entry

    # Test getting specific criterion scores
    for criterion, expected_score in zip(criteria, score_values):
        response = client.get(f"/job_offers/{offer_id}/applicants/{applicant_id}/scores/{criterion['id']}")
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        score_entry = data["score"]
        assert "score" in score_entry
        assert score_entry["score"] == expected_score
        assert "applicant_id" in score_entry
        assert score_entry["applicant_id"] == applicant_id
        assert "criteria_id" in score_entry
        assert score_entry["criteria_id"] == criterion["id"]
        assert "created_at" in score_entry


def test_get_score_for_nonexistent_applicant(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Data Scientist"})
    offer_id = response.json()["job_offer"]["id"]

    # Attempt to retrieve scores for a non-existent applicant
    response = client.get(f"/job_offers/{offer_id}/applicants/9999/scores")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_update_applicant_score(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Data Scientist"})
    offer_id = response.json()["job_offer"]["id"]

    # Create criteria for the job offer
    criteria = [
        {"description": "Experience in data science", "importance": 0.6},
        {"description": "Proficiency in Python", "importance": 0.4},
    ]
    response = client.post(f"/job_offers/{offer_id}/criteria", json={"criteria": criteria})
    criteria = response.json()["criteria"]

    # Create an applicant for the job offer
    cv_text = "Name: Alice Smith\nExperience: 4 years in data science\nSkills: Python, R, SQL"
    response = client.post(f"/job_offers/{offer_id}/applicants", json={"applicants": [{"cv": cv_text}]})
    applicant_id = response.json()["applicants"][0]["id"]

    # Create the scores directly in the database (there's no endpoint for this)
    from recruitair.api import app
    from recruitair.database import get_db_session
    from recruitair.database.models import ApplicantScore

    # Get the get_db dependency
    # This is a workaround to access the database session
    db_dependency = app.dependency_overrides.get(get_db_session)
    score_values = [0.8, 0.9]  # Example scores for the criteria
    db = next(db_dependency())
    scores = []
    for criterion, score_value in zip(criteria, score_values):
        score = ApplicantScore(
            criteria_id=criterion["id"],
            applicant_id=applicant_id,
            score=score_value,
        )
        scores.append(score)
    db.add_all(scores)
    db.commit()
    db.close()

    new_score_values = [0.95, 0.85]

    # Test getting specific criterion scores
    for criterion, new_score_value in zip(criteria, new_score_values):
        response = client.put(
            f"/job_offers/{offer_id}/applicants/{applicant_id}/scores/{criterion['id']}",
            json={"score": new_score_value},
        )
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        score_entry = data["score"]
        assert "score" in score_entry
        assert score_entry["score"] == new_score_value
        assert "applicant_id" in score_entry
        assert score_entry["applicant_id"] == applicant_id
        assert "criteria_id" in score_entry
        assert score_entry["criteria_id"] == criterion["id"]
        assert "created_at" in score_entry

    # Check that they have been updated
    for criterion, expected_score in zip(criteria, new_score_values):
        response = client.get(f"/job_offers/{offer_id}/applicants/{applicant_id}/scores/{criterion['id']}")
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        score_entry = data["score"]
        assert "score" in score_entry
        assert score_entry["score"] == expected_score
        assert "applicant_id" in score_entry
        assert score_entry["applicant_id"] == applicant_id
        assert "criteria_id" in score_entry
        assert score_entry["criteria_id"] == criterion["id"]
        assert "created_at" in score_entry
