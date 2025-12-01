from fastapi.testclient import TestClient

from recruitair.api import app

# ------------- JOB OFFER TESTS ------------- #


def test_create_job_offer(client: TestClient):
    response = client.post("/job_offers", json={"text": "Junior Data Scientist"})
    assert response.status_code == 200

    data = response.json()
    assert "job_offer" in data
    assert "message" in data
    assert data["job_offer"]["text"] == "Junior Data Scientist"
    assert data["job_offer"]["status"] == "PENDING"
    assert "created_at" in data["job_offer"]
    assert "id" in data["job_offer"]


def test_create_job_offer_invalid(client: TestClient):
    response = client.post("/job_offers", json={})
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()
    assert {
        "detail": [{"type": "missing", "loc": ["body", "text"], "msg": "Field required", "input": {}}]
    } == response.json()


def test_list_all_job_offers(client: TestClient):
    # First, create several job offers to ensure there's at least one
    texts = []
    for buzz_word_1 in ["AI", "Blockchain", "Cloud", "DevOps", "Full-Stack", "Data"]:
        for buzz_word_2 in ["Engineer", "Specialist", "Architect", "Analyst", "Consultant"]:
            text = f"{buzz_word_1} {buzz_word_2}"
            texts.append(text)
            client.post("/job_offers", json={"text": text})

    response = client.get("/job_offers", params={"offset": 0, "limit": 1000})
    assert response.status_code == 200

    data = response.json()
    assert "job_offers" in data
    assert isinstance(data["job_offers"], list)
    assert len(data["job_offers"]) == len(texts)
    for offer in data["job_offers"]:
        assert "id" in offer
        assert "text" in offer
        assert "status" in offer
        assert "created_at" in offer


# def test_update_job_offer():
#     # Create one first
#     create = client.post("/job_offers", json={"text": "Backend Engineer"})
#     offer_id = create.json()["job_offer"]["id"]

#     response = client.put(f"/job_offers/{offer_id}", json={"criteria": "Python"})
#     assert response.status_code == 200
#     assert "Updated successfully" in response.json()["message"]


# # ------------- APPLICANT TESTS ------------- #


# def test_create_applicant():
#     response = client.post("/applicants", json={"cv": {"name": "John Doe", "experience": "2 years"}})
#     assert response.status_code == 200
#     assert "applicant" in response.json()


# def test_get_applicant():
#     response = client.get("/applicants")
#     assert response.status_code == 200
#     assert "applicants" in response.json()


# def test_update_applicant():
#     create = client.post("/applicants", json={"cv": {"name": "Jane Doe"}})
#     applicant_id = create.json()["applicant"]["id"]

#     response = client.put(f"/applicants/{applicant_id}", json={"scores": {"technical": 8, "communication": 7}})
#     assert response.status_code == 200
#     assert "Updated successfully" in response.json()["message"]
