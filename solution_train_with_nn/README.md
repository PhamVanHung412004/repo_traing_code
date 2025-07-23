# Hướng dẫn cài đặt và chạy mô hình phân loại văn bản

## 1. Cài đặt môi trường

Khuyến nghị sử dụng Python 3.11 và môi trường ảo (virtualenv hoặc conda).

### Cài đặt các thư viện cần thiết

```bash
pip install -r solution_train_with_nn/setup.txt
```

## 2. Chạy kiểm thử mô hình

```bash
python3 solution_train_with_nn/test.py
```

- Nếu muốn chạy trên CPU, không cần chỉnh gì thêm.
- Nếu muốn chạy trên GPU, sửa dòng sau trong `test.py`:
  ```python
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  ```

## 3. Cấu trúc thư mục

- `solution_train_with_nn/model/model_state.pth`: Trọng số mô hình đã huấn luyện
- `solution_train_with_nn/vocal/vocab.pkl`: Từ điển (vocab) đã lưu
- `solution_train_with_nn/test.py`: File kiểm thử mô hình
- `solution_train_with_nn/setup.txt`: Danh sách thư viện cần cài đặt

## 4. Lưu ý
- Đảm bảo các file dữ liệu và mô hình đúng vị trí như trên.
- Nếu gặp lỗi về phiên bản, hãy kiểm tra lại các phiên bản torch và torchtext như trong file `setup.txt`. 