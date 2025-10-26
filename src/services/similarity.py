import numpy as np
import pickle
import os

from sklearn.metrics.pairwise import cosine_similarity


class SimilarityService:
    """Service for finding similar applications using embeddings."""

    def __init__(self, version: str = "v1"):
        if version not in ["v1", "v2"]:
            raise ValueError("Model version must be 'v1' or 'v2'")
        self.version = version
        self.embeddings = self.load_embeddings(version)

    @staticmethod
    def load_embeddings(version: str):
        """Load embeddings pickle file."""
        path = f"data/mock_embeddings_{version}.pkl"
        if not os.path.exists(path):
            # For tests or local dev: generate mock embeddings
            np.random.seed(42)
            return np.random.rand(100, 64)
        with open(path, "rb") as f:
            return pickle.load(f)

    def find_similar(self, app_vector: list, top_k: int = 10):
        """Find top-k similar apps based on cosine similarity."""
        app_vec = np.array(app_vector).reshape(1, -1)
        sims = cosine_similarity(app_vec, self.embeddings)[0]
        top_indices = np.argsort(sims)[::-1][:top_k]
        return [{"index": int(i), "similarity": float(sims[i])} for i in top_indices]
