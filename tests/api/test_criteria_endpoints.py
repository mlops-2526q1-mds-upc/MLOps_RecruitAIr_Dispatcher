from fastapi.testclient import TestClient

# # ------------- APPLICANT TESTS ------------- #


def test_create_criteria(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Backend Engineer"})
    offer_id = response.json()["job_offer"]["id"]

    criteria = [
        {"description": "Experience in backend development", "importance": 0.5},
        {"description": "Proficiency in Python and FastAPI", "importance": 0.5},
    ]

    response = client.post(f"/job_offers/{offer_id}/criteria", json={"criteria": criteria})
    assert response.status_code == 200
    data = response.json()

    assert "criteria" in data
    assert "message" in data
    assert len(data["criteria"]) == len(criteria)
    for criterion_input, criterion in zip(criteria, data["criteria"]):
        assert "description" in criterion
        assert "importance" in criterion
        assert "id" in criterion
        assert "offer_id" in criterion
        assert "created_at" in criterion
        assert criterion["description"] == criterion_input["description"]
        assert criterion["importance"] == criterion_input["importance"]
        assert criterion["offer_id"] == offer_id
