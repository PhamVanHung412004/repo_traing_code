# 🚀 Email Classifier Server Starter

Tự động khởi động Backend và Frontend server cho ứng dụng Email Classifier.

## 📋 Tính năng

- ✅ **Tự động khởi động**: Backend (Flask) và Frontend (HTTP server)
- 🔍 **Kiểm tra dependencies**: Tự động kiểm tra các packages cần thiết
- 📁 **Kiểm tra files**: Đảm bảo tất cả files cần thiết tồn tại
- 🌐 **Mở trình duyệt**: Tự động mở frontend trong trình duyệt
- 🛑 **Dừng an toàn**: Nhấn Ctrl+C để dừng tất cả servers
- 📊 **Giám sát**: Theo dõi trạng thái các servers

## 🎯 Cách sử dụng

### **Phương pháp 1: Python Script (Khuyến nghị)**

```bash
# Linux/Mac
python3 start_server.py

# Windows
python start_server.py
```

### **Phương pháp 2: Shell Script (Linux/Mac)**

```bash
./start_server.sh
```

## 📊 Thông tin Servers

Sau khi khởi động thành công:

- 🌐 **Frontend**: http://localhost:8000
- 🔧 **Backend**: http://localhost:5000
- 📧 **API Endpoint**: http://localhost:5000/email

## 🔧 Yêu cầu hệ thống

### **Dependencies cần thiết:**
- Python 3.7+
- Flask
- Flask-CORS
- scikit-learn
- numpy

### **Files cần thiết:**
- `backend/api_sever.py`
- `backend/model/improved_email_classifier.pkl`
- `fontend/index.html`
- `fontend/styles.css`
- `fontend/script.js`

## 📦 Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Quy trình khởi động

1. **Kiểm tra dependencies** → Đảm bảo tất cả packages đã cài
2. **Kiểm tra files** → Đảm bảo tất cả files tồn tại
3. **Khởi động Backend** → Flask server tại port 5000
4. **Khởi động Frontend** → HTTP server tại port 8000
5. **Mở trình duyệt** → Tự động mở http://localhost:8000
6. **Giám sát** → Theo dõi trạng thái servers

## 🛑 Dừng servers

Nhấn **Ctrl+C** trong terminal để dừng tất cả servers an toàn.

## 🔍 Troubleshooting

### **Lỗi "Thiếu packages"**
```bash
pip install -r requirements.txt
```

### **Lỗi "Thiếu files"**
- Kiểm tra cấu trúc thư mục
- Đảm bảo model file tồn tại
- Kiểm tra tên file có đúng không

### **Port đã được sử dụng**
- Dừng các processes khác đang sử dụng port 5000/8000
- Hoặc thay đổi port trong code

### **Backend không khởi động**
- Kiểm tra model file `improved_email_classifier.pkl`
- Kiểm tra dependencies Flask
- Xem log lỗi trong terminal

### **Frontend không load**
- Kiểm tra file HTML/CSS/JS có đúng không
- Mở Developer Tools (F12) để xem lỗi
- Kiểm tra console errors

## 📁 Cấu trúc file

```
Chung_ket_trang_code/
├── start_server.py          # Python script chính
├── start_server.sh          # Shell script (Linux/Mac)
├── start_server.bat         # Batch script (Windows)
├── README_SERVER.md         # Hướng dẫn này
├── requirements.txt         # Dependencies
├── backend/
│   ├── api_sever.py        # Flask backend
│   └── model/
│       └── improved_email_classifier.pkl
└── fontend/
    ├── index.html          # Frontend HTML
    ├── styles.css          # CSS styling
    └── script.js           # JavaScript logic
```

## 🎯 Sử dụng ứng dụng

1. **Mở frontend**: http://localhost:8000
2. **Nhập email**: Gõ nội dung email vào ô textarea
3. **Phân tích**: Click "Phân tích Email" hoặc Ctrl+Enter
4. **Xem kết quả**: Dự đoán, độ tin cậy, xác suất

## 📝 Email mẫu

Có sẵn 3 loại email mẫu để test:
- **Email thường**: Email hợp lệ, bình thường
- **Email spam**: Email quảng cáo, spam
- **Email lừa đảo**: Email giả mạo, phishing

## 🔧 Tùy chỉnh

### **Thay đổi ports**
Chỉnh sửa trong `start_server.py`:
```python
# Backend port
process = subprocess.Popen([sys.executable, 'api_sever.py'])

# Frontend port
process = subprocess.Popen([sys.executable, '-m', 'http.server', '8000'])
```

### **Thêm dependencies**
Chỉnh sửa trong `start_server.py`:
```python
required_packages = [
    'flask', 'flask-cors', 'scikit-learn', 'numpy'
]
```

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra log trong terminal
2. Đảm bảo tất cả dependencies đã cài
3. Kiểm tra cấu trúc thư mục
4. Restart servers nếu cần

## 📄 License

MIT License - Tự do sử dụng và chỉnh sửa. 