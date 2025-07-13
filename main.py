from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

# Load model
try:
    model = joblib.load('base_model_random_forest.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Mapping kategori cuti
cuti_mapping = {'aktif': 0, 'non-aktif': 1, 'cuti': 2}

# Inisialisasi Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Prediksi Kelulusan Mahasiswa API',
        'status': 'active',
        'endpoint': '/predict',
        'method': 'POST'
    })

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Ambil input dan konversi ke DataFrame
    try:
        required_fields = ['ips_1', 'ips_2', 'ips_3', 'ips_4', 'cuti_1', 'cuti_2', 'cuti_3', 'cuti_4', 'total_sks_ditempuh', 'total_sks_tidak_lulus']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

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

        return jsonify({
            'prediction': int(prediction),
            'label': label,
            'confidence_score': round(confidence, 3)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Get port from environment variable or default to 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 