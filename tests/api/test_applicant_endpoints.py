from fastapi.testclient import TestClient

# # ------------- APPLICANT TESTS ------------- #


def test_create_applicants(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Backend Engineer"})
    offer_id = response.json()["job_offer"]["id"]

    cv_texts = [
        "Name: John Doe\nExperience: 5 years in backend development\nSkills: Python, FastAPI, SQLAlchemy",
        "Name: Mary Anne\nExperience: 6 years in backend development\nSkills: Python, FastAPI, SQLAlchemy",
    ]

    response = client.post(f"/job_offers/{offer_id}/applicants", json={"applicants": [{"cv": cv} for cv in cv_texts]})
    assert response.status_code == 200
    data = response.json()

    assert "applicants" in data
    assert "message" in data
    assert len(data["applicants"]) == len(cv_texts)
    for cv_text, applicant in zip(cv_texts, data["applicants"]):
        assert "cv" in applicant
        assert "id" in applicant
        assert "offer_id" in applicant
        assert "created_at" in applicant
        assert applicant["cv"] == cv_text
        assert applicant["offer_id"] == offer_id
        assert isinstance(applicant["id"], int)


def test_create_applicant_invalid_offer(client: TestClient):
    invalid_offer_id = 9999
    cv_text = "Name: John Doe\nExperience: 5 years in backend development\nSkills: Python, FastAPI, SQLAlchemy"

    response = client.post(f"/job_offers/{invalid_offer_id}/applicants", json={"applicants": [{"cv": cv_text}]})
    assert response.status_code == 404


def test_create_applicant_missing_fields(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Backend Engineer"})
    offer_id = response.json()["job_offer"]["id"]

    # Test missing applicants altogether
    response = client.post(f"/job_offers/{offer_id}/applicants", json={})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert {
        "detail": [{"type": "missing", "loc": ["body", "applicants"], "msg": "Field required", "input": {}}]
    } == response.json()

    # Test applicant is missing 'cv' field
    response = client.post(f"/job_offers/{offer_id}/applicants", json={"applicants": [{}]})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert {
        "detail": [{"type": "missing", "loc": ["body", "applicants", 0, "cv"], "msg": "Field required", "input": {}}]
    } == response.json()


def test_get_applicants_for_offer(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Backend Engineer"})
    offer_id = response.json()["job_offer"]["id"]

    cv_texts = [
        "Name: John Doe\nExperience: 5 years in backend development\nSkills: Python, FastAPI, SQLAlchemy",
        "Name: Mary Anne\nExperience: 6 years in backend development\nSkills: Python, FastAPI, SQLAlchemy",
    ]

    # Create applicants
    client.post(f"/job_offers/{offer_id}/applicants", json={"applicants": [{"cv": cv} for cv in cv_texts]})

    # Retrieve applicants
    response = client.get(f"/job_offers/{offer_id}/applicants")
    assert response.status_code == 200
    data = response.json()

    assert "applicants" in data
    assert len(data["applicants"]) == len(cv_texts)
    for cv_text, applicant in zip(cv_texts, data["applicants"]):
        assert "cv" in applicant
        assert "id" in applicant
        assert "offer_id" in applicant
        assert "created_at" in applicant
        assert applicant["cv"] == cv_text
        assert applicant["offer_id"] == offer_id
