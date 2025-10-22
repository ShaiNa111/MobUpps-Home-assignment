# MobUpps Similarity API

## Table of content
* [Overview](#overview)
* [System Structure](#system-structure)
* [Service Architecture Diagram](#service-architecture-diagram)
* [API Endpoints](#api-endpoints)
* [Technical Decisions & Rationale](#technical-decisions--rationale)
* [Testing & Local Run](#testing--local-run)
* [CI/CD Workflow Overview](#cicd-workflow-overview)

## Overview

This project implements a production-ready FastAPI microservice for finding similar mobile apps based on precomputed embeddings, running A/B testing between two model versions (v1 & v2), and exposing REST endpoints for inference and performance metrics.

The service demonstrates:

* ML system design for an AdTech similarity search pipeline 
* A/B traffic routing and performance tracking
* Containerized deployment (Docker)
* Unit tests using pytest
* Designed for scaling to millions of requests/day

##  System Structure
```
your_solution/
├── src/
│   ├── services/
│   │   ├── similarity.py        # Handles embedding loading and cosine similarity
│   │   └── ab_testing.py        # Routes requests between v1/v2 and tracks metrics
│   └── api/
│       └── endpoints.py         # FastAPI routes and orchestration
│
├── tests/
│   ├── test_similarity.py       # Unit tests for similarity logic
│   ├── test_ab_testing.py       # Unit tests for A/B router
│   └── test_api.py              # Integration tests for endpoints
│
├── docker/
│   ├── requirements.txt             # Dependencies
│   ├── Dockerfile               # Container build file
│   └── docker-compose.yml       # Local container orchestration
│ 
└── README.md                    # Project documentation

```

## Service Architecture Diagram
```
               ┌───────────────────────────┐
               │       Client / API        │
               │ (Advertiser or internal)  │
               └──────────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ FastAPI (Uvicorn/ECS)  │
                  │  - /find-similar       │
                  │  - /metrics            │
                  └───────────┬────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │  A/B Router                     │
             │  (v1=70%, v2=30%)               │
             └─────────────────────────────────┘
                              │
                 ┌────────────────────┐
                 │ Similarity Service │
                 │  - Loads embeddings│
                 │  - Computes cosine │
                 └────────────────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │        Metrics         │
                 └────────────────────────┘

```

## API Endpoints

| Method   | Endpoint        | Description                                               |
| -------- | --------------- | --------------------------------------------------------- |
| **GET**  | `/health`       | Health check for liveness probe                           |
| **POST** | `/find-similar` | Returns top-K most similar apps using cosine similarity   |
| **GET**  | `/metrics`      | Returns latency and performance metrics per model version |

Example Request:
```
POST /find-similar
{
  "vector": [
        0.37454012, 0.95071431, 0.73199394, 0.59865848, 0.15601864, 0.15599452,
        0.05808361, 0.86617615, 0.60111501, 0.70807258, 0.02058449, 0.96990985,
        0.83244264, 0.21233911, 0.23182197, 0.18340451, 0.30424224, 0.52475643,
        0.43194502, 0.29122914, 0.61185289, 0.13949386, 0.29214465, 0.36636184,
        0.45606998, 0.78517596, 0.19967378, 0.51423444, 0.59241457, 0.04645041,
        0.60754485, 0.17052412, 0.06505159, 0.94888554, 0.96563203, 0.80839735,
        0.30461377, 0.09767211, 0.68423303, 0.44015249, 0.12203823, 0.49517691,
        0.03438852, 0.9093204, 0.25877998, 0.66252228, 0.31171108, 0.52006802,
        0.54671028, 0.18485446, 0.96958463, 0.77513282, 0.93949894, 0.89482735,
        0.59789998, 0.92187424, 0.0884925, 0.19598286, 0.04522729, 0.32533033,
        0.38867729, 0.27134903, 0.82873751, 0.35675333
    ]
}

```

Example Response:
```
{
  "model_version": "v1",
  "results": [
    {"index": 23, "similarity": 0.943},
    {"index": 56, "similarity": 0.921}
  ]
}

```


## Technical Decisions & Rationale
1. FastAPI Framework
   * Lightweight, async-ready, type-safe (via Pydantic), and integrates well with ML workloads. 
   * Trade-off: Slightly more verbose setup than Flask, but faster and better suited for modern async microservices.

2. Embedding Search via Cosine Similarity
   * For simplicity and transparency — ideal for small to medium datasets. 
   * Trade-off: Linear search (O(n)) not ideal for large-scale (>1M items).
   * Future Optimization: Replace with FAISS / Annoy / ScaNN for vector indexing (sub-10ms queries at scale).

3. A/B Testing Framework
   * Needed to compare mock_embeddings_v1 vs. mock_embeddings_v2 performance fairly.
   * Design: Random traffic split (default 70/30), configurable via YAML.
   * Trade-off: Basic traffic routing; doesn’t yet include significance testing or reward optimization (could be extended with Bayesian bandits).

4. Dockerized Microservice
   * Ensures reproducibility, deployability, and isolation.
   * Trade-off: Slight overhead for local dev, but essential for production parity.

5. Testing Strategy 
   * Unit tests: Validate logic for similarity search & A/B routing.
   * Integration tests: Validate endpoint behavior via FastAPI’s TestClient.
   * Goal: Guarantee <200ms response latency under light load.


## Testing & Local Run
Run locally
```bash
  uvicorn src.api.endpoints:app --host 0.0.0.0 --port 8080 --reload
```

Run tests
```bash
  PYTHONPATH=. pytest -v
```

Docker run
```bash
    docker-compose up --build
```

## CI/CD Workflow Overview
I choose to divid it to some parts to make it easy to understand the process.

#### 1. Development Phase
Developers creates or updates code and once ready, the developer pushes the branch to GitHub when the tests pass locally, after that the code is pushed for review.

#### 2. Continuous Integration (CI)
**Using:** GitHub Actions (or any CI tool like Jenkins, GitLab CI, Azure DevOps)</br>
What happens automatically on every push or pull request:
1. Checkout & Setup 
   * Pulls the latest code. 
   * Sets up the Python environment (e.g., installs dependencies from requirements.txt). 
2. Linting & Static Checks
   * Tools like flake8 or pylint ensure code quality and style.
3. Run Unit Tests
   * Runs all tests in /tests. 
   * Fails immediately if any test or import breaks.
4. Build Docker Image
   * Dockerfile from /docker/ is used to package the app.
   
**Final Result:** If all checks pass, the branch is approved for merging into main.

#### 3. Continuous Delivery (CD)
**Using:** GitHub Actions / Cloud Build / Azure Pipeline

Once code is merged into main, CD takes over:

1. Build Stage
   * The microservice is packaged into a production-ready Docker image. 
   * Tagged with version and commit hash (mobupps-similarity:v1.2.3).
2. Push to Container Registry
   * Image is pushed to a registry like Docker Hub, GCP Artifact Registry, or Azure Container Registry.
3. Deploy to Staging
   * The new image is deployed to a staging environment (e.g., a test server or Kubernetes namespace).
   * Health checks and integration tests run to confirm behavior.

**Final Result:** If all staging checks pass → automatic or manual approval for production.

#### 4. Continuous Deployment (Production)
**Using:** CD System + Infrastructure (Kubernetes / ECS / Azure Web App)
Once approved:
* The new version of the API is deployed gradually:
  * Blue/Green Deployment: new version (blue) runs alongside old one (green).
  * Traffic slowly shifts to the new version.
  * If no issues → old version is shut down.

* Autoscaling ensures system stability:
  * If traffic spikes (e.g., 10× users), Kubernetes scales pods automatically.
* Monitoring tools (Prometheus, Grafana, CloudWatch) track:
  * Latency 
  * Request errors 
  * CPU/memory usage
