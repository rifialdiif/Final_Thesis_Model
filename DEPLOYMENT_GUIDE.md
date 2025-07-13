# 🚀 RF_Lupa-Wak! API - Deployment Guide

Panduan lengkap untuk deploy REST API Machine Learning ke Google Cloud Platform (GCP).

## 📋 Prerequisites

### 1. Google Cloud Platform Account

- Buat akun GCP di [console.cloud.google.com](https://console.cloud.google.com)
- Aktifkan billing untuk project Anda

### 2. Install Google Cloud SDK

```bash
# Windows (PowerShell)
# Download dari: https://cloud.google.com/sdk/docs/install

# macOS
brew install google-cloud-sdk

# Linux
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 3. Install Docker

```bash
# Download dari: https://docs.docker.com/get-docker/
```

## 🔧 Setup Project

### 1. Clone Repository

```bash
git clone https://github.com/rifialdiif/Final_Thesis_Model.git
cd Final_Thesis_Model
```

### 2. Setup GCP Project

```bash
# Login ke GCP
gcloud auth login

# Buat project baru (opsional)
gcloud projects create YOUR_PROJECT_ID --name="RF Lupa-Wak API"

# Set project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## 🚀 Deployment Methods

### Method 1: Manual Deployment (Recommended for first time)

#### Step 1: Update Project ID

Edit file `deploy.sh` dan ganti `PROJECT_ID=""` dengan project ID Anda:

```bash
PROJECT_ID="your-project-id-here"
```

#### Step 2: Run Deployment Script

```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### Method 2: Step by Step Manual

#### Step 1: Build Docker Image

```bash
docker build -t gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api .
```

#### Step 2: Push to Container Registry

```bash
docker push gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api
```

#### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy rf-lupa-wak-api \
  --image gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

### Method 3: Automated Deployment with Cloud Build

#### Step 1: Connect GitHub to Cloud Build

1. Buka [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Klik "Connect Repository"
3. Pilih GitHub dan authorize
4. Pilih repository `rifialdiif/Final_Thesis_Model`

#### Step 2: Create Trigger

1. Klik "Create Trigger"
2. Name: `rf-lupa-wak-api-trigger`
3. Event: `Push to a branch`
4. Branch: `main`
5. Source: Repository yang sudah di-connect
6. Build configuration: `Cloud Build configuration file (yaml or json)`
7. Cloud Build configuration file location: `cloudbuild.yaml`

#### Step 3: Push Changes

```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

## 🧪 Testing

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Test API
python test_api.py
```

### Remote Testing

```bash
# Get your API URL
API_URL=$(gcloud run services describe rf-lupa-wak-api --region=asia-southeast1 --format="value(status.url)")

# Test health check
curl $API_URL

# Test prediction
curl -X POST $API_URL/predict \
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

## 📊 Monitoring & Logs

### View Logs

```bash
gcloud logs read --filter resource.type="cloud_run_revision" --limit=50
```

### Monitor Performance

1. Buka [Cloud Run Console](https://console.cloud.google.com/run)
2. Pilih service `rf-lupa-wak-api`
3. Lihat metrics di tab "Metrics"

## 🔧 Configuration

### Environment Variables

- `PORT`: Port server (default: 5000)
- `PYTHONUNBUFFERED`: Python output buffering (set to 1)

### Resource Limits

- Memory: 512Mi
- CPU: 1 core
- Max Instances: 10
- Region: asia-southeast1

## 🛠️ Troubleshooting

### Common Issues

#### 1. Permission Denied

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Check authentication
gcloud auth list
```

#### 2. Docker Build Failed

```bash
# Check Docker is running
docker --version

# Build with verbose output
docker build -t gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api . --progress=plain
```

#### 3. Model Loading Error

- Pastikan file `base_model_random_forest.pkl` ada di root directory
- Check file permissions

#### 4. API Not Responding

```bash
# Check service status
gcloud run services describe rf-lupa-wak-api --region=asia-southeast1

# View logs
gcloud logs read --filter resource.type="cloud_run_revision" --limit=20
```

## 💰 Cost Optimization

### Free Tier

- Cloud Run: 2 million requests/month
- Container Registry: 0.5 GB storage
- Cloud Build: 120 build-minutes/day

### Cost Monitoring

1. Buka [Billing Console](https://console.cloud.google.com/billing)
2. Set up budget alerts
3. Monitor usage in real-time

## 🔄 Updates & Maintenance

### Update Deployment

```bash
# Build new image
docker build -t gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api .

# Push to registry
docker push gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api

# Deploy update
gcloud run deploy rf-lupa-wak-api \
  --image gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api \
  --region asia-southeast1
```

### Rollback

```bash
# List revisions
gcloud run revisions list --service=rf-lupa-wak-api --region=asia-southeast1

# Rollback to previous version
gcloud run services update-traffic rf-lupa-wak-api \
  --to-revisions=REVISION_NAME=100 \
  --region=asia-southeast1
```

## 📞 Support

Jika mengalami masalah:

1. Check logs: `gcloud logs read`
2. Verify configuration di `app.py`
3. Test locally terlebih dahulu
4. Pastikan semua dependencies terinstall

## 🎯 Next Steps

Setelah deployment berhasil:

1. Integrate dengan frontend aplikasi
2. Set up monitoring dan alerting
3. Implement rate limiting jika diperlukan
4. Add authentication jika diperlukan
5. Set up CI/CD pipeline untuk automated deployment
