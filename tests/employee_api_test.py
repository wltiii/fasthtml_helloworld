from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from mocks.employee_api import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def restore_mock_database():
    """
    Pytest fixture that automatically runs before each test.

    This fixture makes a deep copy of the mock database before each test
    and then restores it after each test. This ensures that the mock
    database is reset to its original state after each test, which is
    useful for tests that modify the mock database.

    The fixture is marked with autouse=True, which means that it will
    automatically be run before each test, without needing to be
    explicitly mentioned in the test's parameter list.
    """
    global mock_database
    from mocks.employee_api import mock_database
    original_mock_database = deepcopy(mock_database)
    yield
    mock_database.clear()  # Clear the mock_database
    mock_database.update(original_mock_database)

def test_get_record():
    response = client.get("/api/records/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "John Doe"

def test_get_record_not_found():
    response = client.get("/api/records/9")
    assert response.status_code == 404

def test_create_record():
    data = {"name": "New Employee", "email": "new@example.com", "role": "User"}
    response = client.post("/api/records", json=data)
    assert response.status_code == 200
    assert response.json()["id"] > 3
    assert response.json()["id"] == 4

# def test_update_record():
#     data = {"field": "name", "value": "Updated Name"}
#     response = client.put("/api/records/1", json=data)
#     assert response.status_code == 200
#     assert response.json()["name"] == "Updated Name"

def test_delete_record():
    response = client.delete("/api/records/1")
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_get_records():
    response = client.get("/api/records")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_filter_records_filtered_by_name():
    response = client.get("/api/records?name=John")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_filter_records_filtered_by_lowercased_name():
    response = client.get("/api/records?name=john")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_filter_records_filtered_by_mixed_case_name():
    response = client.get("/api/records?name=jOhN")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_records_filtered_by_email():
    response = client.get("/api/records?email=jane@example.com")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_records_filtered_by_role():
    response = client.get("/api/records?role=User")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_records_compound_filtered_by_role_and_email():
    response = client.get("/api/records?role=Admin&email=jane@example.com")
    assert response.status_code == 200
    assert len(response.json()) == 2
