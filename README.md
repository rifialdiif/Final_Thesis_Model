# RF_Lupa-Wak! - Prediction API

This repository contains a machine learning model developed as part of my final project to classify the graduation status of students in the Software Engineering (TRPL) program at Politeknik Enjinering Indorama (PEI).

## API Endpoints

### Health Check

- **GET** `/` - Check if the API is running
- Response: JSON with status and model loading information

### Prediction

- **POST** `/predict` - Predict graduation status
- Request Body (JSON):

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

- Response (JSON):

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
2. Project ID: `finalthesis-465407`
3. Repository pushed to GitHub

### Deployment Steps

1. **Clone repository and navigate to project directory:**

```bash
git clone https://github.com/rifialdiif/Final_Thesis_Model.git
cd Final_Thesis_Model
```

2. **Set up Google Cloud project:**

```bash
gcloud config set project finalthesis-465407
```

3. **Enable required APIs:**

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

4. **Deploy to Cloud Run:**

```bash
gcloud run deploy prediction-api \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

5. **Get the service URL:**

```bash
gcloud run services describe prediction-api --region asia-southeast1 --format="value(status.url)"
```

### Testing the API

Once deployed, you can test the API using curl:

```bash
# Health check
curl https://your-service-url/

# Prediction
curl -X POST https://your-service-url/predict \
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

## Model Information

- **Algorithm**: Random Forest
- **Features**: IPS (1-4), Cuti status (1-4), Total SKS ditempuh, Total SKS tidak lulus
- **Target**: Graduation status (Lulus Tepat Waktu / Lulus Tidak Tepat Waktu)
