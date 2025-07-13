# 🔄 Port Change Documentation

## 📝 Perubahan Port dari 8080 ke 5000

Project ini telah dikonfigurasi untuk menggunakan **port 5000** sebagai default, menggantikan port 8080.

## 🔧 File yang Diperbarui

### 1. `app.py`

```python
# Sebelum
port = int(os.environ.get('PORT', 8080))

# Sesudah
port = int(os.environ.get('PORT', 5000))
```

### 2. `Dockerfile`

```dockerfile
# Sebelum
EXPOSE 8080
ENV PORT=8080

# Sesudah
EXPOSE 5000
ENV PORT=5000
```

### 3. Testing Files

- `test_api.py` - Default URL: `http://localhost:5000`
- `example_usage.py` - Default URL: `http://localhost:5000`

### 4. Documentation Files

- `README.md` - Updated curl examples
- `QUICK_START.md` - Updated local testing commands
- `DEPLOYMENT_GUIDE.md` - Updated environment variables
- `SUMMARY.md` - Updated configuration

## 🚀 Deployment Impact

### Local Development

```bash
# Run locally (akan menggunakan port 5000)
python app.py
# Server akan berjalan di http://localhost:5000
```

### Cloud Run Deployment

- **Tidak ada perubahan** untuk deployment di Cloud Run
- Cloud Run akan otomatis menggunakan port yang diset di environment variable `PORT`
- Jika tidak ada environment variable, akan menggunakan port 5000

### Docker Container

```bash
# Build dan run container
docker build -t rf-lupa-wak-api .
docker run -p 5000:5000 rf-lupa-wak-api
# API akan accessible di http://localhost:5000
```

## 🧪 Testing dengan Port Baru

### Local Testing

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

### Automated Testing

```bash
# Test dengan script
python test_api.py

# Test dengan custom URL
python test_api.py http://localhost:5000
```

## ⚠️ Important Notes

### 1. Environment Variable Override

Anda masih bisa override port dengan environment variable:

```bash
# Gunakan port custom
PORT=3000 python app.py
```

### 2. Cloud Run Compatibility

- Cloud Run akan otomatis set `PORT` environment variable
- Tidak perlu perubahan untuk deployment di GCP

### 3. Docker Compatibility

- Container akan expose port 5000
- Bisa di-override saat run:

```bash
docker run -p 3000:5000 rf-lupa-wak-api
```

## 🔍 Verification

### Check Current Port

```bash
# Cek port yang digunakan
netstat -tulpn | grep :5000
# atau
lsof -i :5000
```

### Test API

```bash
# Test health check
curl http://localhost:5000/

# Expected response:
{
  "status": "healthy",
  "message": "RF_Lupa-Wak! API is running",
  "model_loaded": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

## 📊 Benefits of Port 5000

1. **Common Development Port** - Port 5000 sering digunakan untuk development
2. **Less Conflicts** - Mengurangi konflik dengan service lain
3. **Standard Practice** - Mengikuti best practice untuk Flask apps
4. **Easy to Remember** - Lebih mudah diingat

## 🎯 Next Steps

1. **Test locally** dengan port 5000
2. **Deploy ke GCP** - tidak ada perubahan diperlukan
3. **Update any external references** jika ada
4. **Update documentation** jika diperlukan

## ✅ Checklist

- [x] Update `app.py` default port
- [x] Update `Dockerfile` port configuration
- [x] Update testing files
- [x] Update documentation
- [x] Test local deployment
- [x] Verify Cloud Run compatibility

Port 5000 sekarang menjadi default untuk project ini! 🎉
