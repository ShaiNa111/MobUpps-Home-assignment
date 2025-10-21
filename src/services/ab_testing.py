import random
import numpy as np

from collections import defaultdict


class ABRouter:
    """Handles traffic split and performance metrics."""

    def __init__(self, split: dict = None):
        self.split = split or {"v1": 0.7, "v2": 0.3}
        self.metrics = defaultdict(list)

    def choose_version(self) -> str:
        """Randomly route request based on split ratios."""
        r = random.random()
        return "v1" if r < self.split["v1"] else "v2"

    def log_performance(self, version: str, latency: float):
        """Track performance metrics per version."""
        self.metrics[version].append(latency)

    def get_metrics(self):
        """Return average latency per model version."""
        return {
            version: np.mean(times) if times else 0.0
            for version, times in self.metrics.items()
        }
