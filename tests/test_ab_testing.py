from src.services.ab_testing import ABRouter


def test_choose_version_respects_split():
    router = ABRouter({"v1": 0.5, "v2": 0.5})
    counts = {"v1": 0, "v2": 0}
    for _ in range(1000):
        counts[router.choose_version()] += 1
    assert 400 < counts["v1"] < 600  # roughly balanced


def test_log_and_get_metrics():
    router = ABRouter()
    router.log_performance("v1", 0.1)
    router.log_performance("v1", 0.3)
    router.log_performance("v2", 0.2)
    metrics = router.get_metrics()
    assert round(metrics["v1"], 2) == 0.2
    assert round(metrics["v2"], 2) == 0.2
