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


def test_create_criteria_invalid_offer(client: TestClient):
    invalid_offer_id = 9999

    criteria = [
        {"description": "Experience in backend development", "importance": 0.5},
        {"description": "Proficiency in Python and FastAPI", "importance": 0.5},
    ]

    response = client.post(f"/job_offers/{invalid_offer_id}/criteria", json={"criteria": criteria})
    assert response.status_code == 404
    assert "detail" in response.json()


def test_create_criteria_missing_fields(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Backend Engineer"})
    offer_id = response.json()["job_offer"]["id"]

    # Test missing applicants altogether
    response = client.post(f"/job_offers/{offer_id}/criteria", json={})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert {
        "detail": [{"type": "missing", "loc": ["body", "criteria"], "msg": "Field required", "input": {}}]
    } == response.json()

    # Test applicant is missing 'importance' field
    response = client.post(f"/job_offers/{offer_id}/criteria", json={"criteria": [{"description": "Some description"}]})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "criteria", 0, "importance"],
                "msg": "Field required",
                "input": {"description": "Some description"},
            }
        ]
    } == response.json()

    # Test applicant is missing 'description' field
    response = client.post(f"/job_offers/{offer_id}/criteria", json={"criteria": [{"importance": 0.5}]})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "criteria", 0, "description"],
                "msg": "Field required",
                "input": {"importance": 0.5},
            }
        ]
    } == response.json()


def test_get_criteria_for_offer(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Backend Engineer"})
    offer_id = response.json()["job_offer"]["id"]

    criteria = [
        {"description": "Experience in backend development", "importance": 0.5},
        {"description": "Proficiency in Python and FastAPI", "importance": 0.5},
    ]

    response = client.post(f"/job_offers/{offer_id}/criteria", json={"criteria": criteria})

    # Retrieve criteria
    response = client.get(f"/job_offers/{offer_id}/criteria")
    assert response.status_code == 200
    data = response.json()

    assert "criteria" in data
    assert len(data["criteria"]) == len(criteria)
    for input_criterion, criterion in zip(criteria, data["criteria"]):
        assert "description" in criterion
        assert "importance" in criterion
        assert "id" in criterion
        assert "offer_id" in criterion
        assert "created_at" in criterion
        assert criterion["description"] == input_criterion["description"]
        assert criterion["importance"] == input_criterion["importance"]
        assert criterion["offer_id"] == offer_id


def test_get_criteria_invalid_offer(client: TestClient):
    invalid_offer_id = 9999

    # Retrieve criteria
    response = client.get(f"/job_offers/{invalid_offer_id}/criteria")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_update_criterion(client: TestClient):
    # Create a job offer first
    response = client.post("/job_offers", json={"text": "Backend Engineer"})
    offer_id = response.json()["job_offer"]["id"]

    criteria = [
        {"description": "Experience in backend development", "importance": 0.5},
    ]

    response = client.post(f"/job_offers/{offer_id}/criteria", json={"criteria": criteria})
    criterion_id = response.json()["criteria"][0]["id"]

    # Update criterion
    updated_data = {"description": "Extensive experience in backend development", "importance": 0.7}
    response = client.put(f"/job_offers/{offer_id}/criteria/{criterion_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()

    assert "criterion" in data
    criterion = data["criterion"]
    assert criterion["id"] == criterion_id
    assert criterion["offer_id"] == offer_id
    assert criterion["description"] == updated_data["description"]
    assert criterion["importance"] == updated_data["importance"]
