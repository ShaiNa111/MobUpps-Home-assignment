import time

from fastapi import FastAPI
from pydantic import BaseModel
from src.services.similarity import SimilarityService
from src.services.ab_testing import ABRouter

app = FastAPI(title="MobUpps Similarity API")
router = ABRouter()


class AppVector(BaseModel):
    vector: list


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return router.get_metrics()


@app.post("/find-similar")
def find_similar(data: AppVector):
    try:
        start = time.time()
        version = router.choose_version()
        service = SimilarityService(version)
        results = service.find_similar(data.vector)
        router.log_performance(version, time.time() - start)
        return {"model_version": version, "results": results}
    except Exception:
        return {"Something went wrong! validate you vector size."}
