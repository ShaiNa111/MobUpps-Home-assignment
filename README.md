# MobUpps Similarity API

### Overview

Production-ready FastAPI microservice for app similarity and A/B testing between two embedding model versions.

### Run Locally

```bash
pip install -r requirements.txt
#uvicorn src.api.endpoints:app --reload
uvicorn src.api.endpoints:app --host 0.0.0.0 --port 8080 --reload
```

### Examples

#### Similiarty API `http://0.0.0.0:8080/find-similar`
GET Request

Example: The first embedding.
```
{
    "vector": [
        0.37454012, 0.95071431, 0.73199394, 0.59865848, 0.15601864, 0.15599452,
        0.05808361, 0.86617615, 0.60111501, 0.70807258, 0.02058449, 0.96990985,
        0.83244264, 0.21233911, 0.18182497, 0.18340451, 0.30424224, 0.52475643,
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

#### Health API `http://0.0.0.0:8080/health`
POST Request

#### Metrics API `http://0.0.0.0:8080/metrics`
GET Request

### Run Tests

```bash
PYTHONPATH=. pytest -v
```
