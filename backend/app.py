from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)


@app.route("/")
def home():
    return jsonify({"message": "Student Management System API is running"})


# =========================
# AUTH
# =========================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "student")

    if not full_name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    cur = mysql.connection.cursor()

    # kiểm tra email đã tồn tại chưa
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        return jsonify({"message": "Email already exists"}), 409

    cur.execute(
        "INSERT INTO users (full_name, email, password, role) VALUES (%s, %s, %s, %s)",
        (full_name, email, hashed_password, role)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, full_name, email, password, role FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user:
        stored_password = user[3]
        if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
            return jsonify({
                "message": "Login success",
                "user": {
                    "id": user[0],
                    "full_name": user[1],
                    "email": user[2],
                    "role": user[4]
                }
            })

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/change-password", methods=["POST"])
def change_password():
    data = request.get_json()

    email = data.get("email")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not email or not old_password or not new_password:
        return jsonify({"message": "Missing required fields"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if not user:
        cur.close()
        return jsonify({"message": "User not found"}), 404

    stored_password = user[0]

    if not bcrypt.checkpw(old_password.encode("utf-8"), stored_password.encode("utf-8")):
        cur.close()
        return jsonify({"message": "Wrong old password"}), 400

    new_hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_hashed, email))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Password updated successfully"})


# =========================
# STUDENTS CRUD
# =========================
@app.route("/students", methods=["GET"])
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    cur.close()

    students = []
    for row in rows:
        students.append({
            "id": row[0],
            "student_code": row[1],
            "full_name": row[2],
            "gender": row[3],
            "dob": str(row[4]) if row[4] else None,
            "phone": row[5],
            "email": row[6]
        })

    return jsonify(students)


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return jsonify({"message": "Student not found"}), 404

    student = {
        "id": row[0],
        "student_code": row[1],
        "full_name": row[2],
        "gender": row[3],
        "dob": str(row[4]) if row[4] else None,
        "phone": row[5],
        "email": row[6]
    }

    return jsonify(student)


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    student_code = data.get("student_code")
    full_name = data.get("full_name")
    gender = data.get("gender")
    dob = data.get("dob")
    phone = data.get("phone")
    email = data.get("email")

    if not student_code or not full_name:
        return jsonify({"message": "Missing required fields"}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO students (student_code, full_name, gender, dob, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (student_code, full_name, gender, dob, phone, email)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student added successfully"}), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()

    student_code = data.get("student_code")
    full_name = data.get("full_name")
    gender = data.get("gender")
    dob = data.get("dob")
    phone = data.get("phone")
    email = data.get("email")

    cur = mysql.connection.cursor()
    cur.execute(
        """
        UPDATE students
        SET student_code=%s, full_name=%s, gender=%s, dob=%s, phone=%s, email=%s
        WHERE id=%s
        """,
        (student_code, full_name, gender, dob, phone, email, student_id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student updated successfully"})


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Student deleted successfully"})


# =========================
# COURSES CRUD
# =========================
@app.route("/courses", methods=["GET"])
def get_courses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    cur.close()

    courses = []
    for row in rows:
        courses.append({
            "id": row[0],
            "course_code": row[1],
            "course_name": row[2],
            "credits": row[3]
        })

    return jsonify(courses)


@app.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json()

    course_code = data.get("course_code")
    course_name = data.get("course_name")
    credits = data.get("credits")

    if not course_code or not course_name or credits is None:
        return jsonify({"message": "Missing required fields"}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO courses (course_code, course_name, credits) VALUES (%s, %s, %s)",
        (course_code, course_name, credits)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Course added successfully"}), 201


@app.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    data = request.get_json()

    course_code = data.get("course_code")
    course_name = data.get("course_name")
    credits = data.get("credits")

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE courses SET course_code=%s, course_name=%s, credits=%s WHERE id=%s",
        (course_code, course_name, credits, course_id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Course updated successfully"})


@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM courses WHERE id=%s", (course_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Course deleted successfully"})


# =========================
# GRADES CRUD
# =========================
@app.route("/grades", methods=["GET"])
def get_grades():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT g.id, s.full_name, c.course_name, g.score
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
    """)
    rows = cur.fetchall()
    cur.close()

    grades = []
    for row in rows:
        grades.append({
            "id": row[0],
            "student_name": row[1],
            "course_name": row[2],
            "score": row[3]
        })

    return jsonify(grades)


@app.route("/grades", methods=["POST"])
def add_grade():
    data = request.get_json()

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    score = data.get("score")

    if not student_id or not course_id or score is None:
        return jsonify({"message": "Missing required fields"}), 400

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO grades (student_id, course_id, score) VALUES (%s, %s, %s)",
        (student_id, course_id, score)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Grade added successfully"}), 201


@app.route("/grades/<int:grade_id>", methods=["PUT"])
def update_grade(grade_id):
    data = request.get_json()

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    score = data.get("score")

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE grades SET student_id=%s, course_id=%s, score=%s WHERE id=%s",
        (student_id, course_id, score, grade_id)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Grade updated successfully"})


@app.route("/grades/<int:grade_id>", methods=["DELETE"])
def delete_grade(grade_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM grades WHERE id=%s", (grade_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Grade deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)