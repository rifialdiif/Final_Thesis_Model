# RF_Lupa-Wak! - ML Model API

This repository contains a machine learning model developed as part of my final project to classify the graduation status of students in the Software Engineering (TRPL) program at Politeknik Enjinering Indorama (PEI).

## API Endpoints

### Health Check

- **GET** `/` - Check if the API is running and model is loaded

### Prediction

- **POST** `/predict` - Predict graduation status

#### Request Body (JSON):

```json
{
  "ips_1": 3.5,
  "ips_2": 3.2,
  "ips_3": 3.8,
  "ips_4": 3.6,
  "cuti_1": "aktif",
  "cuti_2": "aktif",
  "cuti_3": "aktif",
  "cuti_4": "aktif",
  "total_sks_ditempuh": 120,
  "total_sks_tidak_lulus": 0
}
```

#### Response:

```json
{
  "prediction": 0,
  "label": "Lulus Tepat Waktu",
  "confidence_score": 0.85
}
```

## Deployment to Google Cloud Platform

### Prerequisites

1. Google Cloud SDK installed
2. Docker installed
3. Access to GCP project

### Manual Deployment Steps

1. **Enable required APIs:**

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

2. **Build and deploy:**

```bash
# Build the container
docker build -t gcr.io/finalthesis-465407/ml-model-api .

# Push to Container Registry
docker push gcr.io/finalthesis-465407/ml-model-api

# Deploy to Cloud Run
gcloud run deploy ml-model-api \
  --image gcr.io/finalthesis-465407/ml-model-api \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

### Automated Deployment with Cloud Build

1. **Submit build:**

```bash
gcloud builds submit --config cloudbuild.yaml
```

2. **Set up trigger (optional):**

```bash
gcloud builds triggers create github \
  --repo-name=your-repo-name \
  --repo-owner=your-username \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

## Local Development

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Run locally:**

```bash
python app.py
```

3. **Test the API:**

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "ips_1": 3.5,
    "ips_2": 3.2,
    "ips_3": 3.8,
    "ips_4": 3.6,
    "cuti_1": "aktif",
    "cuti_2": "aktif",
    "cuti_3": "aktif",
    "cuti_4": "aktif",
    "total_sks_ditempuh": 120,
    "total_sks_tidak_lulus": 0
  }'
```
