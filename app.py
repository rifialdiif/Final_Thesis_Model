from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import joblib
import numpy as np
import pandas as pd
import os
import logging
from datetime import datetime
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load model
try:
    model = joblib.load('base_model_random_forest.pkl')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

# Mapping kategori cuti
cuti_mapping = {'aktif': 0, 'non-aktif': 1, 'cuti': 2}

# Inisialisasi Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Metrics tracking
request_count = 0
error_count = 0
start_time = datetime.now()

@app.route('/', methods=['GET'])
@limiter.limit("100 per minute")
def health_check():
    """Health check endpoint"""
    global request_count
    request_count += 1
    logger.info("Health check requested")
    return jsonify({
        'status': 'healthy',
        'message': 'RF_Lupa-Wak! API is running',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/docs', methods=['GET'])
@limiter.limit("50 per minute")
def api_docs():
    """API Documentation endpoint"""
    return jsonify({
        'api_name': 'RF_Lupa-Wak! API',
        'version': '1.0.0',
        'description': 'Machine Learning API untuk klasifikasi status kelulusan mahasiswa TRPL',
        'endpoints': {
            'GET /': {
                'description': 'Health check endpoint',
                'response': {
                    'status': 'healthy',
                    'message': 'string',
                    'model_loaded': 'boolean',
                    'timestamp': 'string'
                }
            },
            'GET /metrics': {
                'description': 'System metrics dan monitoring',
                'response': {
                    'uptime_seconds': 'integer',
                    'total_requests': 'integer',
                    'error_count': 'integer',
                    'success_rate': 'float',
                    'system': 'object',
                    'model_loaded': 'boolean',
                    'timestamp': 'string'
                }
            },
            'POST /predict': {
                'description': 'Prediksi status kelulusan',
                'request_body': {
                    'ips_1': 'float (0.0-4.0)',
                    'ips_2': 'float (0.0-4.0)',
                    'ips_3': 'float (0.0-4.0)',
                    'ips_4': 'float (0.0-4.0)',
                    'cuti_1': 'string (aktif/non-aktif/cuti)',
                    'cuti_2': 'string (aktif/non-aktif/cuti)',
                    'cuti_3': 'string (aktif/non-aktif/cuti)',
                    'cuti_4': 'string (aktif/non-aktif/cuti)',
                    'total_sks_ditempuh': 'float (>0)',
                    'total_sks_tidak_lulus': 'float (>=0)'
                },
                'response': {
                    'prediction': 'integer (0/1)',
                    'label': 'string',
                    'confidence_score': 'float (0.0-1.0)',
                    'response_time': 'float'
                }
            }
        },
        'rate_limits': {
            'health_check': '100 per minute',
            'metrics': '10 per minute',
            'predict': '30 per minute'
        },
        'model_info': {
            'algorithm': 'Random Forest Classifier',
            'target': 'Status Kelulusan',
            'labels': {
                '0': 'Lulus Tepat Waktu',
                '1': 'Lulus Tidak Tepat Waktu'
            }
        }
    })

@app.route('/metrics', methods=['GET'])
@limiter.limit("10 per minute")
def metrics():
    """Metrics endpoint for monitoring"""
    global request_count, error_count, start_time
    
    # Get system metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    uptime = datetime.now() - start_time
    
    return jsonify({
        'uptime_seconds': int(uptime.total_seconds()),
        'total_requests': request_count,
        'error_count': error_count,
        'success_rate': round((request_count - error_count) / max(request_count, 1) * 100, 2),
        'system': {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'disk_percent': disk.percent,
            'disk_free_gb': round(disk.free / (1024**3), 2)
        },
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

def validate_input_data(data):
    """Validate input data"""
    errors = []
    
    # Check required fields
    required_fields = ['ips_1', 'ips_2', 'ips_3', 'ips_4', 'cuti_1', 'cuti_2', 'cuti_3', 'cuti_4', 'total_sks_ditempuh', 'total_sks_tidak_lulus']
    for field in required_fields:
        if field not in data:
            errors.append(f'Missing field: {field}')
    
    if errors:
        return errors
    
    # Validate IPS values (0.0 - 4.0)
    for i in range(1, 5):
        field = f'ips_{i}'
        try:
            value = float(data[field])
            if value < 0.0 or value > 4.0:
                errors.append(f'{field} must be between 0.0 and 4.0')
        except (ValueError, TypeError):
            errors.append(f'{field} must be a valid number')
    
    # Validate cuti values
    for i in range(1, 5):
        field = f'cuti_{i}'
        value = data[field].lower() if isinstance(data[field], str) else str(data[field]).lower()
        if value not in cuti_mapping:
            errors.append(f'{field} must be one of: aktif, non-aktif, cuti')
    
    # Validate SKS values
    try:
        total_sks = float(data['total_sks_ditempuh'])
        if total_sks <= 0:
            errors.append('total_sks_ditempuh must be greater than 0')
    except (ValueError, TypeError):
        errors.append('total_sks_ditempuh must be a valid number')
    
    try:
        failed_sks = float(data['total_sks_tidak_lulus'])
        if failed_sks < 0:
            errors.append('total_sks_tidak_lulus must be greater than or equal to 0')
    except (ValueError, TypeError):
        errors.append('total_sks_tidak_lulus must be a valid number')
    
    return errors

@app.route('/predict', methods=['POST'])
@limiter.limit("30 per minute")
def predict():
    global request_count, error_count
    request_count += 1
    start_time = datetime.now()
    logger.info("Prediction request received")
    
    data = request.get_json()

    # Validate input data
    validation_errors = validate_input_data(data)
    if validation_errors:
        error_count += 1
        logger.warning(f"Validation errors: {validation_errors}")
        return jsonify({'error': '; '.join(validation_errors)}), 400

    # Ambil input dan konversi ke DataFrame
    try:
        input_data = {
            'ips_1': float(data['ips_1']),
            'ips_2': float(data['ips_2']),
            'ips_3': float(data['ips_3']),
            'ips_4': float(data['ips_4']),
            'cuti_1': cuti_mapping[data['cuti_1'].lower()],
            'cuti_2': cuti_mapping[data['cuti_2'].lower()],
            'cuti_3': cuti_mapping[data['cuti_3'].lower()],
            'cuti_4': cuti_mapping[data['cuti_4'].lower()],
            'total_sks_ditempuh': float(data['total_sks_ditempuh']),
            'total_sks_tidak_lulus': float(data['total_sks_tidak_lulus'])
        }

        if model is None:
            raise ValueError("Model is not loaded properly.")

        df_input = pd.DataFrame([input_data])
        if not hasattr(model, "predict") or not hasattr(model, "predict_proba"):
            raise AttributeError("Loaded model does not support required methods.")

        prediction = model.predict(df_input)[0]
        confidence = float(model.predict_proba(df_input).max())
        
        # Mapping label hasil prediksi
        label_mapping = {0: 'Lulus Tepat Waktu', 1: 'Lulus Tidak Tepat Waktu'}
        label = label_mapping.get(int(prediction), 'Unknown')

        response_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Prediction completed in {response_time:.3f}s - Result: {label} (confidence: {confidence:.3f})")

        return jsonify({
            'prediction': int(prediction),
            'label': label,
            'confidence_score': round(confidence, 3),
            'response_time': round(response_time, 3)
        })

    except Exception as e:
        error_count += 1
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 400

# Error handler for rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded. Please try again later.',
        'retry_after': e.retry_after
    }), 429

# Jalankan server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
