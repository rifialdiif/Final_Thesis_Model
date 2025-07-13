# 📚 RF_Lupa-Wak! API Documentation

Dokumentasi lengkap untuk REST API Machine Learning klasifikasi status kelulusan mahasiswa TRPL.

## 🌐 Base URL

```
https://rf-lupa-wak-api-xxxxx-xx.a.run.app
```

## 📋 Endpoints

### 1. Health Check

**Endpoint:** `GET /`

**Description:** Memeriksa status API dan model

**Response:**

```json
{
  "status": "healthy",
  "message": "RF_Lupa-Wak! API is running",
  "model_loaded": true
}
```

**Example:**

```bash
curl https://rf-lupa-wak-api-xxxxx-xx.a.run.app/
```

### 2. Prediction

**Endpoint:** `POST /predict`

**Description:** Melakukan prediksi status kelulusan berdasarkan data mahasiswa

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

**Field Descriptions:**

| Field                   | Type   | Description                   | Valid Values                 |
| ----------------------- | ------ | ----------------------------- | ---------------------------- |
| `ips_1`                 | float  | IPK semester 1                | 0.0 - 4.0                    |
| `ips_2`                 | float  | IPK semester 2                | 0.0 - 4.0                    |
| `ips_3`                 | float  | IPK semester 3                | 0.0 - 4.0                    |
| `ips_4`                 | float  | IPK semester 4                | 0.0 - 4.0                    |
| `cuti_1`                | string | Status cuti semester 1        | "aktif", "non-aktif", "cuti" |
| `cuti_2`                | string | Status cuti semester 2        | "aktif", "non-aktif", "cuti" |
| `cuti_3`                | string | Status cuti semester 3        | "aktif", "non-aktif", "cuti" |
| `cuti_4`                | string | Status cuti semester 4        | "aktif", "non-aktif", "cuti" |
| `total_sks_ditempuh`    | float  | Total SKS yang sudah ditempuh | > 0                          |
| `total_sks_tidak_lulus` | float  | Total SKS yang tidak lulus    | >= 0                         |

**Success Response:**

```json
{
  "prediction": 0,
  "label": "Lulus Tepat Waktu",
  "confidence_score": 0.85
}
```

**Error Response:**

```json
{
  "error": "Missing field: ips_1"
}
```

**Example:**

```bash
curl -X POST https://rf-lupa-wak-api-xxxxx-xx.a.run.app/predict \
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

## 🔍 Response Codes

| Code | Description                          |
| ---- | ------------------------------------ |
| 200  | Success                              |
| 400  | Bad Request (missing/invalid fields) |
| 500  | Internal Server Error                |

## 📊 Prediction Results

### Labels

- `0`: Lulus Tepat Waktu
- `1`: Lulus Tidak Tepat Waktu

### Confidence Score

- Range: 0.0 - 1.0
- Semakin tinggi nilai, semakin yakin prediksi

## 🧪 Testing Examples

### Example 1: Mahasiswa dengan IPK Tinggi

```json
{
  "ips_1": 3.8,
  "ips_2": 3.9,
  "ips_3": 3.7,
  "ips_4": 3.8,
  "cuti_1": "aktif",
  "cuti_2": "aktif",
  "cuti_3": "aktif",
  "cuti_4": "aktif",
  "total_sks_ditempuh": 144,
  "total_sks_tidak_lulus": 0
}
```

**Expected Result:** `Lulus Tepat Waktu` dengan confidence tinggi

### Example 2: Mahasiswa dengan IPK Rendah

```json
{
  "ips_1": 2.0,
  "ips_2": 2.1,
  "ips_3": 2.3,
  "ips_4": 2.2,
  "cuti_1": "aktif",
  "cuti_2": "aktif",
  "cuti_3": "aktif",
  "cuti_4": "aktif",
  "total_sks_ditempuh": 120,
  "total_sks_tidak_lulus": 15
}
```

**Expected Result:** `Lulus Tidak Tepat Waktu` dengan confidence tinggi

### Example 3: Mahasiswa dengan Cuti

```json
{
  "ips_1": 3.2,
  "ips_2": 3.1,
  "ips_3": 0.0,
  "ips_4": 3.3,
  "cuti_1": "aktif",
  "cuti_2": "aktif",
  "cuti_3": "cuti",
  "cuti_4": "aktif",
  "total_sks_ditempuh": 90,
  "total_sks_tidak_lulus": 8
}
```

**Expected Result:** `Lulus Tidak Tepat Waktu` (karena ada cuti)

## 🔧 Integration Examples

### Python

```python
import requests
import json

def predict_graduation(data):
    url = "https://rf-lupa-wak-api-xxxxx-xx.a.run.app/predict"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        raise Exception(f"API Error: {response.json()['error']}")

# Example usage
data = {
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

result = predict_graduation(data)
print(f"Prediction: {result['label']}")
print(f"Confidence: {result['confidence_score']}")
```

### JavaScript

```javascript
async function predictGraduation(data) {
  const url = "https://rf-lupa-wak-api-xxxxx-xx.a.run.app/predict";

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const result = await response.json();
      return result;
    } else {
      const error = await response.json();
      throw new Error(error.error);
    }
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

// Example usage
const data = {
  ips_1: 3.5,
  ips_2: 3.2,
  ips_3: 3.8,
  ips_4: 3.6,
  cuti_1: "aktif",
  cuti_2: "aktif",
  cuti_3: "aktif",
  cuti_4: "aktif",
  total_sks_ditempuh: 120,
  total_sks_tidak_lulus: 6,
};

predictGraduation(data)
  .then((result) => {
    console.log(`Prediction: ${result.label}`);
    console.log(`Confidence: ${result.confidence_score}`);
  })
  .catch((error) => {
    console.error("Error:", error);
  });
```

### cURL

```bash
# Health check
curl https://rf-lupa-wak-api-xxxxx-xx.a.run.app/

# Prediction
curl -X POST https://rf-lupa-wak-api-xxxxx-xx.a.run.app/predict \
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

## ⚠️ Error Handling

### Common Errors

1. **Missing Fields**

```json
{
  "error": "Missing field: ips_1"
}
```

2. **Invalid Data Types**

```json
{
  "error": "could not convert string to float: 'invalid'"
}
```

3. **Invalid Cuti Values**

```json
{
  "error": "Invalid cuti value. Must be 'aktif', 'non-aktif', or 'cuti'"
}
```

4. **Model Not Loaded**

```json
{
  "error": "Model is not loaded properly."
}
```

## 📈 Performance

- **Response Time:** < 2 seconds
- **Availability:** 99.9%
- **Rate Limit:** 1000 requests/minute
- **Max Payload:** 1MB

## 🔒 Security

- HTTPS only
- No authentication required (public API)
- Input validation
- Error sanitization

## 📞 Support

Untuk bantuan teknis:

- Email: [your-email@domain.com]
- GitHub Issues: [repository-url]/issues
- Documentation: [this-file-url]
