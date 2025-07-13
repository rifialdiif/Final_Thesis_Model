# RF_Lupa-Wak! - Machine Learning API

This repository contains a machine learning model developed as part of my final project to classify the graduation status of students in the Software Engineering (TRPL) program at Politeknik Enjinering Indorama (PEI).

## Model Information

- **Algorithm**: Random Forest Classifier
- **Target**: Graduation Status Classification (Lulus Tepat Waktu / Lulus Tidak Tepat Waktu)
- **Features**: IPS (GPA) per semester, cuti status, total SKS, and failed SKS

## API Endpoints

### Health Check

```
GET /
```

Returns API status and model loading status.

### Prediction

```
POST /predict
```

**Request Body:**

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
  "total_sks_tidak_lulus": 6
}
```

**Response:**

```json
{
  "prediction": 0,
  "label": "Lulus Tepat Waktu",
  "confidence_score": 0.85
}
```

## Deployment on Google Cloud Platform

### Prerequisites

1. Google Cloud Platform account
2. Google Cloud SDK installed
3. Docker installed (for local testing)

### Manual Deployment Steps

#### 1. Setup GCP Project

```bash
# Login to GCP
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### 2. Build and Deploy

```bash
# Build the Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api .

# Push to Container Registry
docker push gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api

# Deploy to Cloud Run
gcloud run deploy rf-lupa-wak-api \
  --image gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

### Automated Deployment with Cloud Build

1. Connect your GitHub repository to Cloud Build
2. Push changes to trigger automatic deployment
3. Cloud Build will use the `cloudbuild.yaml` configuration

### Environment Variables

- `PORT`: Server port (default: 5000)
- `PYTHONUNBUFFERED`: Python output buffering (set to 1)

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
python app.py
```

### Test API

```bash
# Health check
curl http://localhost:5000/

# Prediction
curl -X POST http://localhost:5000/predict \
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
    "total_sks_tidak_lulus": 6
  }'
```

## Model Performance

- **Accuracy**: [To be added]
- **Precision**: [To be added]
- **Recall**: [To be added]
- **F1-Score**: [To be added]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the final thesis for Software Engineering program at Politeknik Enjinering Indorama.
