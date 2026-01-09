from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Akash*123",
    database="student_db"
)
cursor = db.cursor(dictionary=True)

@app.route("/")
def index():
    name = request.args.get("name")
    branch = request.args.get("branch")
    semester = request.args.get("semester")

    query = "SELECT * FROM students WHERE 1=1"
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

    cursor.execute(query, tuple(params))
    students = cursor.fetchall()

    cursor.execute("SELECT DISTINCT branch FROM students")
    branches = cursor.fetchall()

    return render_template(
        "index.html",
        students=students,
        branches=branches
    )

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
        student_id = request.form["student_id"]
        cursor.execute(
            "INSERT INTO marks (student_id, subject, marks) VALUES (%s,%s,%s)",
            (student_id, request.form["subject"], request.form["marks"])
        )
        db.commit()
        return redirect("/")
    return render_template("marks.html", student_id=id)

@app.route("/marks/view/<int:id>")
def view_marks(id):
    cursor.execute(
        "SELECT subject, marks FROM marks WHERE student_id=%s",
        (id,)
    )
    records = cursor.fetchall()
    return render_template("view_marks.html", records=records)

@app.route("/delete/<int:id>")
def delete_student(id):
    # Delete attendance records first
    cursor.execute("DELETE FROM attendance WHERE student_id=%s", (id,))
    
    # Delete marks records
    cursor.execute("DELETE FROM marks WHERE student_id=%s", (id,))
    
    # Delete student
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    
    db.commit()
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)