import numpy as np

from src.services.similarity import SimilarityService


def test_similarity_returns_topk_results():
    service = SimilarityService(version="v1")
    app_vector = np.random.rand(64).tolist()
    results = service.find_similar(app_vector, top_k=5)
    assert len(results) == 5
    assert all("index" in r and "similarity" in r for r in results)
    assert 0 <= results[0]["similarity"] <= 1


def test_invalid_version_raises_error():
    try:
        SimilarityService(version="v3")
    except ValueError as e:
        assert "version must be" in str(e).lower()
