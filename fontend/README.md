# Email Classifier Frontend

Giao diện web hiện đại để phân loại email sử dụng AI.

## Tính năng

- 🎨 **Giao diện hiện đại**: Thiết kế đẹp mắt với gradient và animation
- 📱 **Responsive**: Hoạt động tốt trên desktop và mobile
- ⚡ **Tương tác mượt mà**: Loading states và error handling
- 🎯 **Kết quả chi tiết**: Hiển thị dự đoán, độ tin cậy và xác suất
- 📝 **Email mẫu**: Có sẵn các email mẫu để thử nghiệm
- 🌐 **API Integration**: Kết nối với Flask backend

## Cách sử dụng

### 1. Khởi động Backend
```bash
cd backend
python api_sever.py
```
Backend sẽ chạy tại `http://localhost:5000`

### 2. Mở Frontend
Mở file `index.html` trong trình duyệt web hoặc sử dụng local server:

```bash
# Sử dụng Python
python -m http.server 8000

# Hoặc sử dụng Node.js
npx serve .

# Hoặc sử dụng PHP
php -S localhost:8000
```

Sau đó truy cập: `http://localhost:8000`

### 3. Sử dụng ứng dụng

1. **Nhập email**: Gõ nội dung email vào ô textarea
2. **Phân tích**: Click nút "Phân tích Email" hoặc dùng Ctrl+Enter
3. **Xem kết quả**: Kết quả sẽ hiển thị với:
   - Dự đoán loại email
   - Độ tin cậy (confidence)
   - Xác suất các loại khác nhau

### 4. Email mẫu
Có sẵn 3 loại email mẫu để thử nghiệm:
- **Email thường**: Email hợp lệ, bình thường
- **Email spam**: Email quảng cáo, spam
- **Email lừa đảo**: Email giả mạo, phishing

## Cấu trúc file

```
fontend/
├── index.html          # Trang chính
├── styles.css          # CSS styling
├── script.js           # JavaScript logic
└── README.md           # Hướng dẫn này
```

## API Endpoint

Frontend gọi API tại: `http://localhost:5000/email`

**Request:**
```json
{
  "message": "Nội dung email cần phân tích"
}
```

**Response:**
```json
{
  "response": {
    "prediction": "spam",
    "confidence": 0.95,
    "probabilities": {
      "spam": 0.95,
      "ham": 0.05
    }
  }
}
```

## Tùy chỉnh

### Thay đổi API URL
Trong file `script.js`, thay đổi:
```javascript
const API_BASE_URL = 'http://localhost:5000';
```

### Thêm email mẫu
Trong file `script.js`, chỉnh sửa mảng `sampleEmails`:
```javascript
const sampleEmails = [
    {
        name: "Tên email mẫu",
        content: "Nội dung email mẫu"
    }
];
```

### Thay đổi giao diện
Chỉnh sửa file `styles.css` để thay đổi màu sắc, font, layout.

## Troubleshooting

### Lỗi CORS
Nếu gặp lỗi CORS, đảm bảo backend đã cài đặt Flask-CORS:
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

### Backend không chạy
Kiểm tra:
- Backend đã chạy tại port 5000
- Model file `improved_email_classifier.pkl` tồn tại
- Tất cả dependencies đã được cài đặt

### Frontend không load
- Mở Developer Tools (F12) để xem lỗi
- Kiểm tra console để debug JavaScript
- Đảm bảo tất cả file CSS và JS được load đúng

## Công nghệ sử dụng

- **HTML5**: Cấu trúc trang
- **CSS3**: Styling với Flexbox, Grid, Animations
- **JavaScript ES6+**: Logic và API calls
- **Font Awesome**: Icons
- **Google Fonts**: Typography

## License

MIT License - Tự do sử dụng và chỉnh sửa. 