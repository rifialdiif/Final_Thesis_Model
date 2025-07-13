# Prediksi Kelulusan Mahasiswa API

API untuk memprediksi kelulusan mahasiswa menggunakan model Machine Learning Random Forest.

## Fitur

- Prediksi kelulusan mahasiswa (Lulus Tepat Waktu / Lulus Tidak Tepat Waktu)
- Confidence score untuk setiap prediksi
- REST API yang mudah digunakan

## Deployment di Google Cloud Platform

### Prerequisites

1. Install Google Cloud SDK
2. Login ke Google Cloud: `gcloud auth login`
3. Set project: `gcloud config set project finalthesis-465407`

### Langkah-langkah Deployment

1. **Clone repository**

```bash
git clone https://github.com/rifialdiif/Final_Thesis_Model.git
cd Final_Thesis_Model
```

2. **Deploy ke Cloud Run**

```bash
gcloud run deploy prediksi-kelulusan-api \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10
```

3. **Atau deploy menggunakan App Engine**

```bash
gcloud app deploy app.yaml
```

### Penggunaan API

#### Endpoint: `/predict`

**Method:** POST
**Content-Type:** application/json

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

### Field Requirements

- `ips_1` sampai `ips_4`: IP Semester 1-4 (float)
- `cuti_1` sampai `cuti_4`: Status cuti semester 1-4 ("aktif", "non-aktif", "cuti")
- `total_sks_ditempuh`: Total SKS yang sudah ditempuh (float)
- `total_sks_tidak_lulus`: Total SKS yang tidak lulus (float)

### Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run locally:

```bash
python main.py
```

3. Test API:

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
    "total_sks_ditempuh": 144,
    "total_sks_tidak_lulus": 0
  }'
```
