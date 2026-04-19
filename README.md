 ## Student Management System API

##  Giới thiệu
Đây là hệ thống quản lý sinh viên được xây dựng bằng **Flask (Python)** và **MySQL**.  
Hệ thống cung cấp các API để:
- Đăng ký / đăng nhập
- Quản lý sinh viên (CRUD)
- Đổi mật khẩu

---

##  Công nghệ sử dụng
- Python 3.14
- Flask
- MySQL
- Postman (test API)
- Git & GitHub

---

##  Cấu trúc project


StudentManagementSystem/
│
├── backend/
│ ├── app.py
│ ├── config.py
│ ├── requirements.txt
│ └── venv/
│
├── database/
│ └── sms_db.sql
│
└── README.md


---

##  Cài đặt

### 1. Clone project

```bash
git clone https://github.com/binhhocembedded/ProgAndTest_Group03.git
cd ProgAndTest_Group03
2. Tạo môi trường ảo
cd backend
py -m venv venv
source venv/Scripts/activate   # Windows
3. Cài thư viện
pip install -r requirements.txt
4. Setup database
Mở phpMyAdmin
Tạo database: sms_db
Import file:
database/sms_db.sql
5. Cấu hình kết nối MySQL

Trong config.py:

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'sms_db'
6. Chạy server
python app.py

 Server chạy tại:

http://127.0.0.1:5000
 API Endpoints
 Auth
1. Register
POST /register

Body:

{
  "full_name": "Cam Tu",
  "email": "tu@gmail.com",
  "password": "123456"
}
2. Login
POST /login

Body:

{
  "email": "tu@gmail.com",
  "password": "123456"
}
3. Change Password
POST /change-password

Body:

{
  "email": "tu@gmail.com",
  "old_password": "123456",
  "new_password": "abc123"
}
 Student
1. Create student
POST /students
2. Get all students
GET /students
3. Get student by ID
GET /students/<id>
4. Update student
PUT /students/<id>
5. Delete student
DELETE /students/<id>
 Test API

Sử dụng:

Postman
hoặc trình duyệt (GET)
 Lưu ý
Không push thư mục venv/
Không push file .env
Dùng .gitignore
 Tác giả
Nguyễn Cẩm Tú (Backend)
Nhóm ProgAndTest_Group03
