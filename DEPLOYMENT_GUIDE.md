# 🚀 Panduan Lengkap Deployment ML Model ke GCP Cloud Run

## 📋 Prerequisites

Sebelum memulai deployment, pastikan Anda telah menginstall:

1. **Google Cloud SDK** - [Download here](https://cloud.google.com/sdk/docs/install)
2. **Docker** - [Download here](https://docs.docker.com/get-docker/)
3. **Git** (opsional) - [Download here](https://git-scm.com/downloads)

## 🔧 Setup Awal

### 1. Install Google Cloud SDK

```bash
# Download dan install Google Cloud SDK
# Setelah install, jalankan:
gcloud init
```

### 2. Login ke Google Cloud

```bash
gcloud auth login
gcloud config set project finalthesis-465407
```

### 3. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

## 🚀 Deployment Methods

### Method 1: Menggunakan Script Otomatis (Recommended)

1. **Buat script executable:**

```bash
chmod +x deploy.sh
```

2. **Jalankan deployment:**

```bash
./deploy.sh
```

### Method 2: Manual Deployment

1. **Build Docker Image:**

```bash
docker build -t gcr.io/finalthesis-465407/ml-model-api .
```

2. **Push ke Container Registry:**

```bash
docker push gcr.io/finalthesis-465407/ml-model-api
```

3. **Deploy ke Cloud Run:**

```bash
gcloud run deploy ml-model-api \
  --image gcr.io/finalthesis-465407/ml-model-api \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

### Method 3: Menggunakan Cloud Build

1. **Submit build:**

```bash
gcloud builds submit --config cloudbuild.yaml
```

## 🧪 Testing

### 1. Test Local (Sebelum Deploy)

```bash
# Install dependencies
pip install -r requirements.txt

# Run aplikasi
python app.py

# Test dengan script
python test_api.py
```

### 2. Test API yang Sudah Deploy

Setelah deployment selesai, Anda akan mendapatkan URL API. Test dengan:

```bash
# Health check
curl -X GET https://your-service-url-here

# Prediction
curl -X POST https://your-service-url-here/predict \
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

## 📊 Monitoring & Logs

### 1. View Logs

```bash
gcloud logs read --filter resource.type="cloud_run_revision" --limit=50
```

### 2. Monitor Service

```bash
gcloud run services describe ml-model-api --region=asia-southeast1
```

### 3. View Metrics di Console

- Buka [Cloud Run Console](https://console.cloud.google.com/run)
- Pilih service `ml-model-api`
- Lihat metrics di tab "Metrics"

## 🔧 Configuration

### Environment Variables

Jika perlu menambahkan environment variables:

```bash
gcloud run services update ml-model-api \
  --region=asia-southeast1 \
  --set-env-vars KEY=VALUE
```

### Scaling Configuration

```bash
gcloud run services update ml-model-api \
  --region=asia-southeast1 \
  --min-instances=0 \
  --max-instances=10 \
  --cpu=1 \
  --memory=1Gi
```

## 🛠️ Troubleshooting

### Common Issues:

1. **Docker build failed**

   - Pastikan Docker berjalan
   - Check Dockerfile syntax
   - Pastikan semua file ada

2. **Permission denied**

   - Jalankan `gcloud auth configure-docker`
   - Pastikan login dengan `gcloud auth login`

3. **Service not accessible**

   - Check `--allow-unauthenticated` flag
   - Verify region setting
   - Check service logs

4. **Model loading error**
   - Pastikan file `base_model_random_forest.pkl` ada
   - Check model file size dan format

### Debug Commands:

```bash
# Check service status
gcloud run services list --region=asia-southeast1

# View detailed logs
gcloud logs read --filter resource.type="cloud_run_revision" --limit=100

# Test locally with Docker
docker run -p 8080:8080 gcr.io/finalthesis-465407/ml-model-api
```

## 💰 Cost Optimization

### Tips untuk menghemat biaya:

1. **Set min-instances ke 0** (default)
2. **Gunakan max-instances yang reasonable** (10-20)
3. **Monitor usage** di Cloud Console
4. **Set up billing alerts**

### Estimated Costs:

- **Cloud Run**: ~$0.00002400 per 100ms
- **Container Registry**: ~$0.026 per GB per month
- **Network**: ~$0.12 per GB

## 🔄 Update Deployment

Untuk update aplikasi:

1. **Build new image:**

```bash
docker build -t gcr.io/finalthesis-465407/ml-model-api .
```

2. **Push dan deploy:**

```bash
docker push gcr.io/finalthesis-465407/ml-model-api
gcloud run deploy ml-model-api --image gcr.io/finalthesis-465407/ml-model-api --region=asia-southeast1
```

## 📞 Support

Jika mengalami masalah:

1. Check logs dengan `gcloud logs read`
2. Verify configuration di Cloud Console
3. Test locally terlebih dahulu
4. Check Google Cloud documentation

## 🎯 Next Steps

Setelah deployment berhasil:

1. **Set up monitoring** dengan Cloud Monitoring
2. **Configure alerts** untuk error dan performance
3. **Set up CI/CD** dengan Cloud Build triggers
4. **Add authentication** jika diperlukan
5. **Optimize performance** berdasarkan usage patterns
