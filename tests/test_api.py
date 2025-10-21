from fastapi.testclient import TestClient
from src.api.endpoints import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_find_similar_endpoint():
    data = {"vector": [0.1]*64}
    r = client.post("/find-similar", json=data)
    assert r.status_code == 200
    result = r.json()
    assert "model_version" in result
    assert "results" in result
    assert len(result["results"]) > 0


def test_metrics_endpoint():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)
