from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "student_secret_key"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash*123",
    database="student_db"
)
cursor = db.cursor(dictionary=True)

@app.route("/")
def index():
    branch = request.args.get("branch")
    semester = request.args.get("semester")

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if branch:
        query += " AND branch = %s"
        params.append(branch)

    if semester:
        query += " AND semester = %s"
        params.append(semester)

    cursor.execute(query, tuple(params))
    students = cursor.fetchall()

    cursor.execute("SELECT DISTINCT branch FROM students")
    branches = cursor.fetchall()

    return render_template("index.html",
                           students=students,
                           branches=branches)

@app.route("/add", methods=["POST"])
def add():
    cursor.execute(
        "INSERT INTO students (name, branch, semester) VALUES (%s,%s,%s)",
        (request.form["name"], request.form["branch"], request.form["semester"])
    )
    db.commit()
    return redirect("/")

@app.route("/attendance/<int:id>", methods=["GET","POST"])
def attendance(id):
    if request.method == "POST":
        student_id = request.form["student_id"]
        cursor.execute(
            "INSERT INTO attendance (student_id, date, status) VALUES (%s,%s,%s)",
            (student_id, request.form["date"], request.form["status"])
        )
        db.commit()
        return redirect("/")
    return render_template("attendance.html", student_id=id)

@app.route("/attendance/view/<int:id>")
def view_attendance(id):
    cursor.execute(
        "SELECT date, status FROM attendance WHERE student_id=%s",
        (id,)
    )
    records = cursor.fetchall()
    return render_template("view_attendance.html", records=records)

@app.route("/marks/<int:id>", methods=["GET","POST"])
def marks(id):
    if request.method == "POST":
        student_id = id
        course_id = request.form["course_id"]
        marks_value = request.form["marks"]

        cursor.execute(
            "INSERT INTO marks (student_id, marks, course_id) VALUES (%s,%s,%s)",
            (student_id, marks_value, course_id)
        )
        db.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()

    return render_template("marks.html", student_id=id, courses=courses)

@app.route("/marks/view/<int:id>")
def view_marks(id):
    cursor.execute("""
        SELECT c.course_name, m.marks
        FROM marks m
        JOIN course c ON m.course_id = c.course_id
        WHERE m.student_id = %s
    """, (id,))
    
    records = cursor.fetchall()
    return render_template("view_marks.html", records=records)

@app.route("/statistics")
def statistics():
    cursor.execute("SELECT COUNT(*) AS total_students FROM students")
    total = cursor.fetchone()

    cursor.execute("SELECT AVG(marks) AS avg_marks FROM marks")
    avg = cursor.fetchone()

    cursor.execute("SELECT MAX(marks) AS max_marks FROM marks")
    maxm = cursor.fetchone()

    cursor.execute("SELECT MIN(marks) AS min_marks FROM marks")
    minm = cursor.fetchone()

    return render_template("statistics.html", total=total, avg=avg, maxm=maxm, minm=minm)

@app.route("/full_details")
def full_details():
    name = request.args.get("name")
    branch = request.args.get("branch")
    semester = request.args.get("semester")
    course = request.args.get("course")
    faculty = request.args.get("faculty")

    query = "SELECT * FROM student_course_view WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE %s"
        params.append(f"%{name}%")

    if branch:
        query += " AND branch = %s"
        params.append(branch)

    if semester:
        query += " AND semester = %s"
        params.append(semester)

    if course:
        query += " AND course_name = %s"
        params.append(course)

    if faculty:
        query += " AND faculty_name = %s"
        params.append(faculty)

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()

    # Get dropdown values
    cursor.execute("SELECT DISTINCT branch FROM students")
    branches = cursor.fetchall()

    cursor.execute("SELECT DISTINCT semester FROM students")
    semesters = cursor.fetchall()

    cursor.execute("SELECT DISTINCT course_name FROM student_course_view")
    courses = cursor.fetchall()

    cursor.execute("SELECT DISTINCT faculty_name FROM student_course_view")
    faculties = cursor.fetchall()

    return render_template("full_details.html",
                           data=data,
                           branches=branches,
                           semesters=semesters,
                           courses=courses,
                           faculties=faculties)

@app.route("/delete/<int:id>")
def delete_student(id):
    try:
        # Only delete attendance (optional)
        cursor.execute("DELETE FROM attendance WHERE student_id=%s", (id,))

        # Do NOT delete marks — let trigger handle protection
        cursor.execute("DELETE FROM students WHERE id=%s", (id,))
        db.commit()
        flash("Student deleted successfully", "success")
    except mysql.connector.Error as err:
        flash("Cannot delete student with marks!", "danger")
    return redirect("/")

@app.route("/grades")
def grades():
    cursor.execute("""
        SELECT s.name,
               AVG(m.marks) AS avg_marks,
               CASE
                   WHEN AVG(m.marks) >= 85 THEN 'A'
                   WHEN AVG(m.marks) >= 70 THEN 'B'
                   WHEN AVG(m.marks) >= 50 THEN 'C'
                   ELSE 'F'
               END AS grade
        FROM students s
        JOIN marks m ON s.id = m.student_id
        GROUP BY s.id
    """)
    records = cursor.fetchall()
    return render_template("grades.html", records=records)

@app.route("/topper")
def topper():
    cursor.execute("""
        SELECT s.name,
               AVG(m.marks) AS avg_marks
        FROM students s
        JOIN marks m ON s.id = m.student_id
        GROUP BY s.id
        ORDER BY avg_marks DESC
        LIMIT 1
    """)
    record = cursor.fetchone()
    return render_template("topper.html", record=record)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if request.method == "POST":
        cursor.execute("""
            UPDATE students
            SET name=%s, branch=%s, semester=%s
            WHERE id=%s
        """, (
            request.form["name"],
            request.form["branch"],
            request.form["semester"],
            id
        ))
        db.commit()
        flash("Student updated successfully!", "success")
        return redirect("/")

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template("edit_student.html", student=student)


@app.route("/courses")
def courses():
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    return render_template("courses.html", courses=courses)

@app.route("/add_course", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course_name = request.form["course_name"]
        faculty_id = request.form["faculty_id"]

        cursor.execute("""
            INSERT INTO course (course_name, faculty_id)
            VALUES (%s, %s)
        """, (course_name, faculty_id))
        db.commit()

        flash("Course added successfully!", "success")
        return redirect("/courses")

    # Load faculty list for dropdown
    cursor.execute("SELECT * FROM faculty")
    faculty = cursor.fetchall()

    return render_template("add_course.html", faculty=faculty)
@app.route("/add_faculty", methods=["GET", "POST"])
def add_faculty():
    if request.method == "POST":
        cursor.execute(
            "INSERT INTO faculty (faculty_name, department) VALUES (%s, %s)",
            (request.form["faculty_name"], request.form["department"])
        )
        db.commit()
        flash("Faculty added successfully!", "success")
        return redirect("/add_faculty")

    cursor.execute("SELECT * FROM faculty")
    faculty = cursor.fetchall()
    return render_template("add_faculty.html", faculty=faculty)

@app.route("/enroll/<int:student_id>", methods=["GET", "POST"])
def enroll(student_id):
    if request.method == "POST":
        course_id = request.form["course_id"]

        cursor.execute(
            "INSERT INTO enrollment (student_id, course_id) VALUES (%s, %s)",
            (student_id, course_id)
        )
        db.commit()
        flash("Student enrolled successfully!", "success")
        return redirect("/")

    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()

    return render_template("enroll.html", courses=courses, student_id=student_id)

@app.route("/attendance_filter", methods=["GET"])
def attendance_filter():
    date = request.args.get("date")
    status = request.args.get("status")

    query = """
        SELECT s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE 1=1
    """
    params = []

    if date:
        query += " AND a.date = %s"
        params.append(date)

    if status:
        query += " AND a.status = %s"
        params.append(status)

    cursor.execute(query, tuple(params))
    records = cursor.fetchall()

    return render_template("attendance_filter.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)