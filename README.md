# Prediksi Kelulusan Mahasiswa API

API untuk memprediksi kelulusan mahasiswa berdasarkan data akademik menggunakan model Random Forest.

## Deployment di Google Cloud Platform

### Langkah-langkah Deployment:

1. **Push ke GitHub**

   ```bash
   git add .
   git commit -m "Prepare for GCP deployment"
   git push origin main
   ```

2. **Setup Google Cloud Project**

   - Buka [Google Cloud Console](https://console.cloud.google.com)
   - Pilih project: `finalthesis-465407`
   - Aktifkan API yang diperlukan:
     - Cloud Run API
     - Cloud Build API
     - Container Registry API

3. **Deploy menggunakan Cloud Build**

   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

4. **Atau deploy manual dengan gcloud**

   ```bash
   # Build dan push image
   gcloud builds submit --tag gcr.io/finalthesis-465407/prediksi-kelulusan-api

   # Deploy ke Cloud Run
   gcloud run deploy prediksi-kelulusan-api \
     --image gcr.io/finalthesis-465407/prediksi-kelulusan-api \
     --platform managed \
     --region asia-southeast1 \
     --allow-unauthenticated \
     --memory 512Mi \
     --cpu 1 \
     --max-instances 10
   ```

## Penggunaan API

### Endpoint: `/predict`

**Method:** POST

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
  "total_sks_ditempuh": 144,
  "total_sks_tidak_lulus": 0
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

### Test dengan curl:

```bash
curl -X POST https://your-cloud-run-url/predict \
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
    "total_sks_ditempuh": 144,
    "total_sks_tidak_lulus": 0
  }'
```

## Field Requirements:

- `ips_1` sampai `ips_4`: IPK semester 1-4 (float)
- `cuti_1` sampai `cuti_4`: Status cuti semester 1-4 ("aktif", "non-aktif", "cuti")
- `total_sks_ditempuh`: Total SKS yang sudah ditempuh (float)
- `total_sks_tidak_lulus`: Total SKS yang tidak lulus (float)
