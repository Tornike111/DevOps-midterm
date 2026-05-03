from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_add_and_retrieve_deployment():
    # Test the POST endpoint
    post_response = client.post("/deployments", json={
        "service_name": "auth-api",
        "build_time_seconds": 120,
        "success": True
    })
    assert post_response.status_code == 200
    deploy_id = post_response.json()["id"]

    # Test the dynamic GET endpoint
    get_response = client.get(f"/deployments/{deploy_id}")
    assert get_response.status_code == 200
    assert get_response.json()["service_name"] == "auth-api"

def test_summary_metrics():
    # Add a failed deployment to test the math
    client.post("/deployments", json={
        "service_name": "payment-worker",
        "build_time_seconds": 80,
        "success": False
    })
    
    response = client.get("/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "average_build_time" in data
    assert "success_rate" in data