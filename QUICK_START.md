# 🚀 Quick Start Guide - RF_Lupa-Wak! API

Panduan cepat untuk deploy REST API Machine Learning ke Google Cloud Platform.

## ⚡ Langkah Cepat (5 Menit)

### 1. Setup GCP Project

```bash
# Install Google Cloud SDK
# Download dari: https://cloud.google.com/sdk/docs/install

# Login ke GCP
gcloud auth login

# Buat project baru (opsional)
gcloud projects create YOUR_PROJECT_ID --name="RF Lupa-Wak API"

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Deploy dengan Script Otomatis

```bash
# Edit PROJECT_ID di deploy.sh
nano deploy.sh
# Ganti PROJECT_ID="" menjadi PROJECT_ID="your-project-id"

# Jalankan deployment
chmod +x deploy.sh
./deploy.sh
```

### 3. Test API

```bash
# Get API URL
API_URL=$(gcloud run services describe rf-lupa-wak-api --region=asia-southeast1 --format="value(status.url)")

# Health check
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

## 🔧 Manual Deployment

### Step 1: Build & Push

```bash
# Build Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api .

# Push to registry
docker push gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api
```

### Step 2: Deploy to Cloud Run

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

## 🧪 Local Testing

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

## 📊 API Endpoints

| Endpoint   | Method | Description         |
| ---------- | ------ | ------------------- |
| `/`        | GET    | Health check        |
| `/docs`    | GET    | API documentation   |
| `/metrics` | GET    | System metrics      |
| `/predict` | POST   | Prediction endpoint |

## 🔍 Monitoring

### View Logs

```bash
gcloud logs read --filter resource.type="cloud_run_revision" --limit=20
```

### Check Metrics

```bash
curl $API_URL/metrics
```

## 🛠️ Troubleshooting

### Common Issues

1. **Permission Denied**

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Model Not Found**

- Pastikan `base_model_random_forest.pkl` ada di root directory

3. **Docker Build Failed**

```bash
docker build -t gcr.io/YOUR_PROJECT_ID/rf-lupa-wak-api . --progress=plain
```

4. **API Not Responding**

```bash
gcloud run services describe rf-lupa-wak-api --region=asia-southeast1
```

## 💰 Cost Estimation

### Free Tier (Bulanan)

- Cloud Run: 2 juta requests
- Container Registry: 0.5 GB storage
- Cloud Build: 120 menit build

### Estimated Cost (Production)

- ~$5-10/bulan untuk 10,000 requests/hari

## 📞 Support

- **Documentation**: `DEPLOYMENT_GUIDE.md`
- **API Docs**: `API_DOCUMENTATION.md`
- **Testing**: `example_usage.py`

## 🎯 Next Steps

1. Set up custom domain
2. Add authentication
3. Implement caching
4. Set up monitoring alerts
5. Add CI/CD pipeline
