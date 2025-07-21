#!/bin/bash

# Email Classifier Backend & Frontend Server Starter
# Khởi động cả Backend và Frontend

echo ""
echo "========================================"
echo "   EMAIL CLASSIFIER BACKEND & FRONTEND STARTER"
echo "========================================"
echo ""

echo "🚀 Khởi động Email Classifier Backend..."
echo ""

# Kiểm tra Python có sẵn không
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được tìm thấy!"
    echo "Vui lòng cài đặt Python3 trước."
    exit 1
fi

# Kiểm tra virtual environment
if [ ! -d "myenv" ]; then
    echo "📦 Tạo virtual environment..."
    python3 -m venv myenv
    echo "✅ Virtual environment đã được tạo!"
fi

# Kích hoạt virtual environment
echo "🔧 Kích hoạt virtual environment..."
source myenv/bin/activate

# Cài đặt requirements
echo "📦 Cài đặt dependencies..."
pip install -r requirements.txt

echo "✅ Tất cả dependencies đã được cài đặt!"
echo ""

# Khởi động Backend server
cd backend
python3 api_sever.py &
BACKEND_PID=$!
cd ..

echo "🔧 Khởi động Frontend server..."
python3 -m http.server 8000 --directory fontend &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "   HỆ THỐNG ĐÃ SẴN SÀNG!"
echo "========================================"
echo ""
echo "🌐 Backend:   http://localhost:5000/"
echo "🌐 Frontend:  http://localhost:8000/index.html"
echo ""
echo "👉 Nhấn Ctrl+C để dừng cả backend và frontend."
echo ""

# Chờ cả hai process
trap "kill $BACKEND_PID $FRONTEND_PID" SIGINT
wait $BACKEND_PID $FRONTEND_PID 