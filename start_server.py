#!/usr/bin/env python3
"""
Email Classifier Server Starter
Tự động khởi động Backend và Frontend server
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path

def print_banner():
    """In banner chào mừng"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    EMAIL CLASSIFIER SERVER                   ║
    ║                                                              ║
    ║  🚀 Tự động khởi động Backend và Frontend                  ║
    ║  📧 Phân loại email thông minh với AI                      ║
    ║  🌐 Frontend: http://localhost:8000                        ║
    ║  🔧 Backend:  https://rang-nguyen-hoi-be.btecit.tech      ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Kiểm tra các dependencies cần thiết"""
    print("🔍 Kiểm tra dependencies...")
    
    # Kiểm tra Python packages
    required_packages = [
        ('flask', 'flask'),
        ('flask_cors', 'flask-cors'),
        ('sklearn', 'scikit-learn'),
        ('numpy', 'numpy')
    ]
    
    missing_packages = []
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Thiếu các packages: {', '.join(missing_packages)}")
        print("📦 Cài đặt bằng lệnh: pip install -r requirements.txt")
        return False
    
    print("✅ Tất cả dependencies đã sẵn sàng!")
    return True

def check_files():
    """Kiểm tra các file cần thiết"""
    print("📁 Kiểm tra files...")
    
    required_files = [
        'backend/api_sever.py',
        'backend/model/improved_email_classifier.pkl',
        'fontend/index.html',
        'fontend/styles.css',
        'fontend/script.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Thiếu các files: {', '.join(missing_files)}")
        return False
    
    print("✅ Tất cả files đã sẵn sàng!")
    return True

def start_backend():
    """Khởi động Backend server"""
    print("🔧 Khởi động Backend server...")
    
    try:
        # Chuyển đến thư mục backend
        os.chdir('backend')
        
        # Khởi động Flask server
        process = subprocess.Popen([
            sys.executable, 'api_sever.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        
        # Đợi một chút để server khởi động
        time.sleep(3)
        
        # Kiểm tra server có chạy không
        if process.poll() is None:
            print("✅ Backend server đã khởi động tại http://localhost:5000")
            return process
        else:
            print("❌ Backend server khởi động thất bại!")
            return None
            
    except Exception as e:
        print(f"❌ Lỗi khởi động Backend: {e}")
        return None

def start_frontend():
    """Khởi động Frontend server"""
    print("🌐 Khởi động Frontend server...")
    
    # Thử các port khác nhau
    ports = [8000, 8001, 8002, 8003, 8004]
    
    for port in ports:
        try:
            # Chuyển đến thư mục frontend
            os.chdir('fontend')
            
            # Kiểm tra port có sẵn không
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"⚠️  Port {port} đã được sử dụng, thử port khác...")
                continue
            
            # Khởi động HTTP server
            process = subprocess.Popen([
                sys.executable, '-m', 'http.server', str(port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Đợi một chút để server khởi động
            time.sleep(2)
            
            # Kiểm tra server có chạy không
            if process.poll() is None:
                print(f"✅ Frontend server đã khởi động tại http://localhost:{port}")
                return process, port
            else:
                print(f"❌ Frontend server khởi động thất bại trên port {port}!")
                continue
                
        except Exception as e:
            print(f"❌ Lỗi khởi động Frontend trên port {port}: {e}")
            continue
    
    print("❌ Không thể khởi động Frontend trên bất kỳ port nào!")
    return None, None

def open_browser(frontend_port=8000):
    """Mở trình duyệt tự động"""
    print("🌐 Mở trình duyệt...")
    time.sleep(3)  # Đợi servers khởi động hoàn toàn
    
    try:
        webbrowser.open(f'http://localhost:{frontend_port}')
        print(f"✅ Đã mở trình duyệt tại http://localhost:{frontend_port}")
    except Exception as e:
        print(f"⚠️  Không thể mở trình duyệt tự động: {e}")
        print(f"🌐 Vui lòng mở trình duyệt và truy cập: http://localhost:{frontend_port}")

def monitor_servers(backend_process, frontend_process, frontend_port=8000):
    """Giám sát các server processes"""
    print("\n🔄 Đang chạy servers... (Nhấn Ctrl+C để dừng)")
    print("📊 Thông tin servers:")
    print(f"   🌐 Frontend: http://localhost:{frontend_port}")
    print("   🔧 Backend:  https://rang-nguyen-hoi-be.btecit.tech")
    print("   📧 API:      https://rang-nguyen-hoi-be.btecit.tech/email")
    print("\n📝 Logs sẽ hiển thị ở đây:")
    print("=" * 60)
    
    try:
        while True:
            # Kiểm tra backend
            if backend_process and backend_process.poll() is not None:
                print("❌ Backend server đã dừng!")
                break
            
            # Kiểm tra frontend
            if frontend_process and frontend_process.poll() is not None:
                print("❌ Frontend server đã dừng!")
                break
            
            # Đọc output từ backend process nếu có
            if backend_process:
                try:
                    # Non-blocking read from stdout
                    import select
                    if select.select([backend_process.stdout], [], [], 0.1)[0]:
                        output = backend_process.stdout.readline()
                        if output:
                            output_str = output.strip()
                            if output_str:  # Chỉ hiển thị nếu có nội dung
                                print(output_str)
                except:
                    pass
            
            # Đọc output từ stderr nếu có
            if backend_process:
                try:
                    import select
                    if select.select([backend_process.stderr], [], [], 0.1)[0]:
                        error_output = backend_process.stderr.readline()
                        if error_output:
                            error_str = error_output.strip()
                            if error_str:  # Chỉ hiển thị nếu có nội dung
                                print(error_str)
                except:
                    pass
            
            time.sleep(1)  # Kiểm tra mỗi giây
            
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng servers...")
        
        # Dừng backend
        if backend_process:
            backend_process.terminate()
            print("✅ Đã dừng Backend server")
        
        # Dừng frontend
        if frontend_process:
            frontend_process.terminate()
            print("✅ Đã dừng Frontend server")
        
        print("👋 Tạm biệt!")

def main():
    """Hàm chính"""
    print_banner()
    
    # Kiểm tra dependencies và files
    if not check_dependencies():
        return
    
    if not check_files():
        return
    
    print("\n🚀 Bắt đầu khởi động servers...\n")
    
    # Lưu thư mục gốc
    root_dir = os.getcwd()
    
    # Khởi động backend trong thread riêng
    backend_process = None
    frontend_process = None
    frontend_port = 8000
    
    try:
        # Khởi động backend
        backend_process = start_backend()
        if not backend_process:
            print("❌ Không thể khởi động Backend!")
            return
        
        # Quay lại thư mục gốc
        os.chdir(root_dir)
        
        # Khởi động frontend
        frontend_result = start_frontend()
        if frontend_result[0] is None:
            print("❌ Không thể khởi động Frontend!")
            backend_process.terminate()
            return
        
        frontend_process, frontend_port = frontend_result
        
        # Quay lại thư mục gốc
        os.chdir(root_dir)
        
        # Mở trình duyệt trong thread riêng
        browser_thread = threading.Thread(target=open_browser, args=(frontend_port,))
        browser_thread.daemon = True
        browser_thread.start()
        
        # Giám sát servers
        monitor_servers(backend_process, frontend_process, frontend_port)
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        
        # Dừng các processes nếu có
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()

if __name__ == "__main__":
    main() 