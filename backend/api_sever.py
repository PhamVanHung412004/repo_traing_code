from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import (
    Dict
)
import re
import pickle
import time
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import csv

# Cấu hình CORS cho domain cụ thể
CORS_ORIGINS = [
    "https://trang-nguyen-hoi-be.btecit.tech",
    "http://trang-nguyen-hoi-be.btecit.tech",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]


class EmailFeatures(BaseEstimator, TransformerMixin):
    """Trích xuất các đặc trưng bổ sung từ email"""
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        features = []
        for text in X:
            feat = {
                'length': len(text),
                'num_exclamation': text.count('!'),
                'num_question': text.count('?'),
                'num_caps': sum(1 for c in text if c.isupper()),
                'caps_ratio': sum(1 for c in text if c.isupper()) / (len(text) + 1),
                'has_url': 1 if 'http' in text.lower() or 'www' in text.lower() else 0,
                'has_email': 1 if '@' in text else 0,
                'num_special_chars': len(re.findall(r'[!@#$%^&*()]', text)),
                'num_currency': len(re.findall(r'[$₫¥€£]', text)),
                'has_discount_words': 1 if any(word in text.lower() for word in 
                    ['giảm giá', 'khuyến mãi', 'sale', 'free', 'miễn phí']) else 0
            }
            features.append(list(feat.values()))
        return np.array(features)

def preprocess_text(text):
    """Tiền xử lý văn bản tiếng Việt"""
    # Loại bỏ HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Loại bỏ URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    # Loại bỏ email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Loại bỏ số điện thoại
    text = re.sub(r'\d{10,}', '', text)
    # Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text)
    return text.lower().strip()

def predict_email(text, model):
    """Dự đoán loại email"""
    processed_text = preprocess_text(text)
    prediction = model.predict([processed_text])[0]
    probabilities = model.predict_proba([processed_text])[0]
    
    return {
        'prediction': prediction,
        'confidence': max(probabilities),
        'probabilities': dict(zip(model.classes_, probabilities))
    }



app = Flask(__name__)

# Cấu hình CORS với middleware
CORS(app, 
     origins=CORS_ORIGINS,
     allow_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-Total-Count"],
     expose_headers=["Content-Type", "X-Total-Count"]
)

# Global variables for statistics
request_count = 0
prediction_stats = {}

with open("model/improved_email_classifier.pkl", "rb") as f:
    model = pickle.load(f)

@app.route('/email', methods=['POST'])
def chat():
    global request_count, prediction_stats
    
    # Lấy dữ liệu từ request và đảm bảo an toàn
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        message = data.get('message', '')
        if not message:
            return jsonify({"error": "Message field is required"}), 400
            
    except Exception as e:
        print(f"❌ Error parsing request data: {e}")
        return jsonify({"error": "Invalid request data format"}), 400
    
    # Update statistics
    request_count += 1
    prediction = predict_email(message, model)
    
    # Update prediction statistics
    pred_type = prediction['prediction']
    if pred_type not in prediction_stats:
        prediction_stats[pred_type] = 0
    prediction_stats[pred_type] += 1
    
    # Log request details
    print(f"📧 Email Analysis Request #{request_count}:")
    print(f"   📝 Content length: {len(message)} characters")
    print(f"   📅 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   🎯 Prediction: {prediction['prediction']}")
    print(f"   📊 Confidence: {prediction['confidence']:.2%}")
    print(f"   📈 Probabilities: {prediction['probabilities']}")
    print(f"   📊 Total requests: {request_count}")
    print(f"   📈 Prediction stats: {prediction_stats}")
    print("-" * 50)
    
    return jsonify(prediction), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    return jsonify({
        "total_requests": request_count,
        "prediction_stats": prediction_stats,
        "server_uptime": time.strftime('%Y-%m-%d %H:%M:%S')
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "model_loaded": model is not None,
        "cors_origins": CORS_ORIGINS,
        "allowed_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allowed_headers": ["Content-Type", "Authorization", "X-Requested-With", "X-Total-Count"]
    }), 200

@app.route('/csv', methods=['GET'])
def get_csv_rows():
    """Trả về một phần dữ liệu từ file CSV với phân trang"""
    try:
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({"error": "Invalid offset or limit"}), 400

    csv_path = "database/data.csv"
    rows = []
    total = 0
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            all_rows = list(reader)
            total = len(all_rows)
            rows = all_rows[offset:offset+limit]
    except Exception as e:
        return jsonify({"error": f"Could not read CSV: {e}"}), 500

    return jsonify({
        "rows": rows,
        "offset": offset,
        "limit": limit,
        "total": total
    }), 200

@app.route('/show_csv', methods=['GET'])
def show_csv():
    csv_path = "database/data.csv"
    rows = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.reader(csvfile))
            rows = reader
    except Exception as e:
        return f"<h3>Lỗi đọc file CSV: {e}</h3>", 500

    # Tạo HTML bảng
    html = "<h2>Bảng dữ liệu CSV</h2><table border='1' style='border-collapse:collapse;'>"
    for i, row in enumerate(rows):
        html += "<tr>"
        for cell in row:
            if i == 0:
                html += f"<th>{cell}</th>"
            else:
                html += f"<td>{cell}</td>"
        html += "</tr>"
    html += "</table>"
    return html

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with CORS information"""
    return jsonify({
        "message": "Email Classification API",
        "cors_enabled": True,
        "allowed_origins": CORS_ORIGINS,
        "endpoints": {
            "email_classification": "/email",
            "health_check": "/health",
            "statistics": "/stats"
        },
        "status": "running"
    }), 200

if __name__ == '__main__':
    # Bật chế độ debug để tự động reload khi có thay đổi code
    app.run(
        host='0.0.0.0',  # Cho phép truy cập từ bên ngoài
        port=5000,
        debug=True,      # Bật chế độ debug và auto-reload
        use_reloader=True,  # Đảm bảo reloader được bật
        threaded=True    # Cho phép xử lý nhiều request đồng thời
    )