import json
from fastapi.testclient import TestClient
from recruitair.api.main import app

client = TestClient(app)


# ------------- JOB OFFER TESTS ------------- #

def test_create_job_offer():
    response = client.post(
        "/job_offers",
        json={"text": "Junior Data Scientist"}
    )
    assert response.status_code == 200
    assert "job_offer" in response.json()


def test_get_job_offers():
    response = client.get("/job_offers?text=Data")
    assert response.status_code == 200
    assert "job_offers" in response.json()


def test_update_job_offer():
    # Create one first
    create = client.post("/job_offers", json={"text": "Backend Engineer"})
    offer_id = create.json()["job_offer"]["id"]

    response = client.put(f"/job_offers/{offer_id}", json={"criteria": "Python"})
    assert response.status_code == 200
    assert "Updated successfully" in response.json()["message"]


# ------------- APPLICANT TESTS ------------- #

def test_create_applicant():
    response = client.post(
        "/applicants",
        json={"cv": {"name": "John Doe", "experience": "2 years"}}
    )
    assert response.status_code == 200
    assert "applicant" in response.json()


def test_get_applicant():
    response = client.get("/applicants")
    assert response.status_code == 200
    assert "applicants" in response.json()


def test_update_applicant():
    create = client.post(
        "/applicants",
        json={"cv": {"name": "Jane Doe"}}
    )
    applicant_id = create.json()["applicant"]["id"]

    response = client.put(
        f"/applicants/{applicant_id}",
        json={"scores": {"technical": 8, "communication": 7}}
    )
    assert response.status_code == 200
    assert "Updated successfully" in response.json()["message"]
