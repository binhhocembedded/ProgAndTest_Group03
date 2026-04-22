# ============================================================
# DOCKERFILE — EduMS Backend + Frontend
# Tác giả phần DevOps: Phan Tấn Dũng
# ============================================================

# BƯỚC 1: Image gốc Python 3.11 nhẹ
FROM python:3.11-slim

# BƯỚC 2: Thư mục làm việc trong container
WORKDIR /app

# BƯỚC 3: Cài thư viện hệ thống
# gcc: để build thư viện C
# pkg-config + libmariadb-dev: để pymysql kết nối MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# BƯỚC 4: Copy requirements.txt trước (tận dụng Docker cache)
# Nếu requirements không đổi → Docker dùng cache, build nhanh hơn
COPY backend/requirements.txt ./requirements.txt

# BƯỚC 5: Cài thư viện Python
# --no-cache-dir: không lưu cache pip → image gọn hơn
RUN pip install --no-cache-dir -r requirements.txt

# BƯỚC 6: Copy toàn bộ source code
COPY backend/ ./backend/
COPY UI_UX/ ./frontend/

# BƯỚC 7: Biến môi trường mặc định
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# BƯỚC 8: Mở cổng Flask
EXPOSE 5000

# BƯỚC 9: Lệnh chạy app khi container khởi động
# --host=0.0.0.0: bắt buộc để có thể truy cập từ ngoài container
CMD ["python", "backend/app.py"]
