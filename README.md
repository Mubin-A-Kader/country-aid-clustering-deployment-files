# Country Aid Clustering API

A Flask API for country aid clustering analysis.

## Quick Start with Docker

1. Build:
```bash
docker build -t country-aid-clustering .
```
2. Run:
```bash
docker run -p 4000:4000 country-aid-clustering.
```

test

curl -X POST http://localhost:4000/predict \
-H "Content-Type: application/json" \
-d '{
    "child_mort": 8.3,
    "exports": 45.2,
    "health": 7.5,
    "imports": 48.6,
    "income": 35000,
    "inflation": 2.5,
    "life_expec": 75.3,
    "total_fer": 1.8,
    "gdpp": 45000,
    "country": "USA"
}'