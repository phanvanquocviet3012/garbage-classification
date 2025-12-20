# ♻️ AI Garbage Classification - Web App

Đây là một ứng dụng Web tích hợp trí tuệ nhân tạo (AI) dùng để phân loại rác thải tự động. Hệ thống sử dụng mô hình được huấn luyện từ **Google Teachable Machine**, triển khai trên nền tảng **Flask** (Backend) và **Streamlit** (Frontend).

## 🚀 Tính năng chính

* **Nhận diện thời gian thực**: Dự đoán loại rác thải thông qua hình ảnh tải lên.
* **Tối ưu hiệu năng**: Sử dụng định dạng **TensorFlow Lite (.tflite)** giúp phản hồi nhanh và nhẹ.
* **Kiến trúc Modular**: Tách biệt hoàn toàn giữa xử lý logic AI (Backend) và giao diện người dùng (Frontend).

## 🛠️ Tech Stack

* **Ngôn ngữ**: Python 3.13
* **AI Framework**: TensorFlow (TFLite)
* **Backend**: Flask, Flask-CORS
* **Frontend**: Streamlit
* **Xử lý ảnh**: Pillow, NumPy

---

## 📂 Cấu trúc thư mục

```text
garbage-classification/
├── backend/                # Server xử lý AI
│   ├── models/             # Chứa model.tflite và labels.txt
│   ├── app_flask.py        # API Flask chính
│   └── utils.py            # Hàm tiền xử lý hình ảnh
├── frontend/               # Giao diện người dùng
│   └── app_streamlit.py    # Giao diện Streamlit kết nối API
├── requirements.txt        # Danh sách thư viện cần thiết
└── README.md

```

---

## 💻 Hướng dẫn cài đặt và sử dụng

### 1. Cài đặt môi trường

Đảm bảo bạn đã cài đặt Python. Mở terminal và chạy lệnh sau để cài đặt các thư viện bổ trợ:

```bash
pip install -r requirements.txt

```

### 2. Khởi chạy hệ thống

Dự án cần chạy 2 terminal song song:

**Bước 1: Chạy Backend (Flask)**

```bash
cd backend
python app_flask.py

```

*Server sẽ mặc định chạy tại: `http://127.0.0.1:5000*`

**Bước 2: Chạy Frontend (Streamlit)**

```bash
cd frontend
streamlit run app_streamlit.py

```

### 3. Cách sử dụng

* Truy cập vào đường dẫn Streamlit cung cấp (thường là `http://localhost:8501`).
* Tải ảnh rác thải lên và nhấn **"Dự đoán"**.
* Kết quả về tên loại rác và độ tin cậy (%) sẽ hiển thị trên màn hình.

---

## 📝 Lưu ý kỹ thuật

* **Pre-processing**: Hình ảnh được resize về kích thước  và chuẩn hóa về khoảng  trước khi đưa vào mô hình.
* **API**: Backend chấp nhận các request POST tại endpoint `/predict` với dữ liệu là `multipart/form-data`.

## 👤 Thông tin tác giả

* **Project**: [Garbage Classification](https://github.com/phanvanquocviet3012/garbage-classification)
