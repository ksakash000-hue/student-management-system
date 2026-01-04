
from flask import Flask, render_template, request, redirect, url_for
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
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    branch = request.form["branch"]
    semester = request.form["semester"]
    cursor.execute(
        "INSERT INTO students (name, branch, semester) VALUES (%s, %s, %s)",
        (name, branch, semester)
    )
    db.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    name = request.form["name"]
    branch = request.form["branch"]
    semester = request.form["semester"]
    cursor.execute(
        "UPDATE students SET name=%s, branch=%s, semester=%s WHERE id=%s",
        (name, branch, semester, id)
    )
    db.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    return redirect(url_for("index"))

@app.route("/search", methods=["POST"])
def search():
    q = request.form["query"]
    cursor.execute(
        "SELECT * FROM students WHERE name LIKE %s OR branch LIKE %s OR semester LIKE %s",
        (f"%{q}%", f"%{q}%", f"%{q}%")
    )
    students = cursor.fetchall()
    return render_template("index.html", students=students)

if __name__ == "__main__":
    app.run(debug=True)
