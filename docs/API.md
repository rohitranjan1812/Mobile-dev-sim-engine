# API Documentation

## Overview

The Mobile Dev Sim Engine provides a RESTful API for property risk assessment and price optimization. All endpoints accept and return JSON data.

## Base URL

```
http://localhost:5000
```

## Endpoints

### Health Check

Check if the API server is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Run Simulation

Run a complete property risk assessment simulation.

**Endpoint:** `POST /api/v1/simulate`

**Request Body:**
```json
{
  "num_samples": 1000,
  "batch_size": 100,
  "random_seed": 42,
  "hazard_weight": 0.4,
  "vulnerability_weight": 0.3,
  "exposure_weight": 0.3
}
```

**Parameters:**
- `num_samples` (integer, optional): Number of samples to generate. Default: 1000
- `batch_size` (integer, optional): Batch size for processing. Default: 100
- `random_seed` (integer, optional): Random seed for reproducibility. Default: null
- `hazard_weight` (float, optional): Weight for hazard factor. Default: 0.4
- `vulnerability_weight` (float, optional): Weight for vulnerability factor. Default: 0.3
- `exposure_weight` (float, optional): Weight for exposure factor. Default: 0.3

**Response:**
```json
{
  "status": "success",
  "num_samples": 1000,
  "risk_statistics": {
    "mean": 0.5002,
    "median": 0.5012,
    "std": 0.1671,
    "min": 0.0325,
    "max": 0.9685,
    "percentile_25": 0.3912,
    "percentile_75": 0.6213,
    "percentile_90": 0.7456,
    "percentile_95": 0.8012,
    "percentile_99": 0.8934
  },
  "price_statistics": {
    "mean": 187500.50,
    "median": 187450.25,
    "std": 20456.78,
    "min": 127890.12,
    "max": 247890.45,
    "total_value": 187500500.00
  }
}
```

---

### Assess Risk

Calculate risk scores for given property factors.

**Endpoint:** `POST /api/v1/assess-risk`

**Request Body:**
```json
{
  "hazard": [0.5, 0.6, 0.3],
  "vulnerability": [0.4, 0.5, 0.2],
  "exposure": [0.3, 0.4, 0.1],
  "weights": {
    "hazard": 0.4,
    "vulnerability": 0.3,
    "exposure": 0.3
  }
}
```

**Parameters:**
- `hazard` (array of floats, required): Hazard values (0-1)
- `vulnerability` (array of floats, required): Vulnerability values (0-1)
- `exposure` (array of floats, required): Exposure values (0-1)
- `weights` (object, optional): Custom risk weights

**Response:**
```json
{
  "status": "success",
  "risk_scores": [0.42, 0.52, 0.21],
  "risk_categories": [1, 2, 0]
}
```

**Risk Categories:**
- 0: Low (< 0.25)
- 1: Medium (0.25 - 0.5)
- 2: High (0.5 - 0.75)
- 3: Very High (>= 0.75)

---

### Optimize Price

Calculate optimized prices based on risk scores.

**Endpoint:** `POST /api/v1/optimize-price`

**Request Body:**
```json
{
  "risk_scores": [0.2, 0.5, 0.8],
  "base_price": 250000
}
```

**Parameters:**
- `risk_scores` (array of floats, required): Risk scores (0-1)
- `base_price` (float, optional): Base property price. Default: 250000

**Response:**
```json
{
  "status": "success",
  "prices": [225000.00, 187500.00, 150000.00]
}
```

---

### Optimize Portfolio

Select optimal properties within budget and risk tolerance.

**Endpoint:** `POST /api/v1/optimize-portfolio`

**Request Body:**
```json
{
  "risk_scores": [0.2, 0.5, 0.8, 0.3],
  "budget": 1000000,
  "risk_tolerance": 0.5
}
```

**Parameters:**
- `risk_scores` (array of floats, required): Risk scores for properties
- `budget` (float, required): Total budget for portfolio
- `risk_tolerance` (float, optional): Maximum acceptable average risk. Default: 0.5

**Response:**
```json
{
  "status": "success",
  "portfolio": {
    "selected_indices": [0, 3],
    "total_cost": 450000.00,
    "average_risk": 0.25,
    "num_properties": 2,
    "remaining_budget": 550000.00
  }
}
```

---

## Error Handling

All endpoints return error responses with status code 400 on failure:

```json
{
  "status": "error",
  "message": "Error description here"
}
```

## Example Usage

### Python
```python
import requests
import json

# Run simulation
response = requests.post(
    'http://localhost:5000/api/v1/simulate',
    json={
        'num_samples': 5000,
        'random_seed': 42
    }
)
data = response.json()
print(f"Mean risk: {data['risk_statistics']['mean']}")
```

### cURL
```bash
curl -X POST http://localhost:5000/api/v1/simulate \
  -H "Content-Type: application/json" \
  -d '{"num_samples": 5000, "random_seed": 42}'
```

## Starting the Server

```bash
python src/api/server.py
```

The server will start on `http://0.0.0.0:5000` by default.
