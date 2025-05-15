# Country Aid Clustering API

A machine learning-based API that analyzes and clusters countries based on various socio-economic indicators to determine their aid requirements and development status.

## Overview

This project implements a clustering algorithm to categorize countries into three distinct risk zones based on multiple development indicators:

- **High Risk Zone (Cluster 1)**: Countries requiring urgent attention for development and stability
- **Moderate Risk (Cluster 0)**: Countries developing steadily but with key areas for improvement
- **Low Risk (Cluster 2)**: Countries showing strong indicators of economic and social well-being

## Features

- Analyzes 9 key development indicators:
  - Child mortality rate
  - Export levels
  - Healthcare spending
  - Import levels
  - National income
  - Inflation rate
  - Life expectancy
  - Total fertility rate
  - GDP per capita
- Real-time country classification
- RESTful API interface
- Docker containerization
- AWS Lambda deployment ready

## Quick Start

### Local Development

1. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

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


## Deploy lambda to mumbai region (ap-south-1)
1. aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <repo-id>.dkr.ecr.ap-south-1.amazonaws.com
2. docker buildx build --platform linux/amd64 --provenance=false -t country-clustering . &&
3. docker tag country-clustering:latest <repo-id>.dkr.ecr.ap-south-1.amazonaws.com/country-clustering:latest &&
4. docker push <repo-id>.dkr.ecr.ap-south-1.amazonaws.com/country-clustering:latest