document.addEventListener("DOMContentLoaded", () => {
   //LOGIN
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            try {
                const res = await fetch("http://localhost:5000/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });
                const data = await res.json();

                if (res.ok) {
                    alert("Đăng nhập thành công!");
                    if (data.user.role === "student") {
                        window.location.href = "student.html";
                    } else if (data.user.role === "teacher") {
                        window.location.href = "teacher.html";
                    } else {
                        window.location.href = "admin.html";
                    }
                } else {
                    alert(data.message || "Sai tài khoản hoặc mật khẩu!");
                }
            } catch (err) {
                console.error(err);
                alert("Không thể kết nối server.");
            }
        });
    }
    //STUDENT DASHBOARD 
    const studentsTable = document.querySelector("#studentsTable tbody");
    if (studentsTable) {
        loadStudents();
    }
    async function loadStudents() {
        try {
            const res = await fetch("http://localhost:5000/students");
            const students = await res.json();
            studentsTable.innerHTML = "";
            students.forEach(s => {
                const row = `<tr>
          <td>${s.student_code}</td>
          <td>${s.full_name}</td>
          <td>${s.gender}</td>
          <td>${s.dob || ""}</td>
          <td>${s.phone || ""}</td>
          <td>${s.email || ""}</td>
        </tr>`;
                studentsTable.innerHTML += row;
            });
        } catch (err) {
            console.error(err);
        }
    }
    //TEACHER DASHBOARD 
    const coursesTable = document.querySelector("#coursesTable tbody");
    if (coursesTable) {
        loadCourses();
    }
    async function loadCourses() {
        try {
            const res = await fetch("http://localhost:5000/courses");
            const courses = await res.json();
            coursesTable.innerHTML = "";
            courses.forEach(c => {
                const row = `<tr>
          <td>${c.course_code}</td>
          <td>${c.course_name}</td>
          <td>${c.credits}</td>
        </tr>`;
                coursesTable.innerHTML += row;
            });
        } catch (err) {
            console.error(err);
        }
    }
    //ADMIN DASHBOARD 
    const gradesTable = document.querySelector("#gradesTable tbody");
    if (gradesTable) {
        loadGrades();
    }

    async function loadGrades() {
        try {
            const res = await fetch("http://localhost:5000/grades");
            const grades = await res.json();
            gradesTable.innerHTML = "";
            grades.forEach(g => {
                const row = `<tr>
          <td>${g.student_name}</td>
          <td>${g.course_name}</td>
          <td>${g.score}</td>
        </tr>`;
                gradesTable.innerHTML += row;
            });
        } catch (err) {
            console.error(err);
        }
    }
});
