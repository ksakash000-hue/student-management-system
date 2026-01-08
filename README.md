# Advanced Student Management System

An Advanced Student Management System developed using Flask (Python) and MySQL.  
This project manages student records along with attendance tracking, marks management, search & filter functionality, and basic UI styling.

---

## Features
- Add, view, and manage student details
- Attendance management (Present / Absent)
- Marks management (subject-wise marks)
- View attendance and marks records
- Search students by name
- Filter students by branch and semester
- Styled user interface using CSS
- Data stored permanently in MySQL database

---

## Technologies Used
- Backend: Flask (Python)
- Database: MySQL
- Frontend: HTML, CSS (Jinja2 Templates)
- IDE: Visual Studio Code
- Version Control: Git & GitHub

---

## Project Structure
Advanced_Student_Management_System/
app.py  
database.sql  
requirements.txt  

templates/
index.html  
attendance.html  
marks.html  
view_attendance.html  
view_marks.html  

static/
style.css  

---

## How to Run the Project

1. Clone the repository  
git clone https://github.com/your-username/Advanced_Student_Management_System.git  

2. Create virtual environment  
python3 -m venv venv  
source venv/bin/activate  

3. Install dependencies  
pip install -r requirements.txt  

4. Setup MySQL database  
mysql -u root -p  
SOURCE database.sql;  

5. Update MySQL password in app.py  
password="YOUR_MYSQL_PASSWORD"  

6. Run the application  
python app.py  

Open browser:  
http://127.0.0.1:5000  

---

## Database Tables
students – stores student details  
attendance – stores attendance records  
marks – stores subject-wise marks  

---

## Academic Purpose
This project is developed as an academic mini project to demonstrate Flask backend development, MySQL database integration, CRUD operations, search & filter functionality, and data visualization.

---

## Author
Akash

---

## License
This project is for educational purposes only.
