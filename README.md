# Student Management System

A simple web-based Student Management System built using **Flask (Python)** and **MySQL**.  
This project is created as an **academic mini project** to perform basic CRUD operations on student records.

## Features
- Add, view, update, and delete student records
- Search student details
- Data stored permanently in MySQL database

## Technologies Used
- Flask (Python)
- MySQL
- HTML, CSS
- Visual Studio Code
- Git & GitHub

## Project Structure
app.py  
requirements.txt  
student_db.sql  
templates/  
.gitignore  

## How to Run
1. Clone the repository  
   `git clone https://github.com/ksakash000-hue/student-management-system.git`

2. Create and activate virtual environment  
   `python3 -m venv venv`  
   `source venv/bin/activate`

3. Install dependencies  
   `pip install -r requirements.txt`

4. Setup database  
   `SOURCE student_db.sql;`

5. Run the application  
   `python app.py`

Open browser:  
`http://127.0.0.1:5000`

## Database Table
**students**  
id | name | branch | semester

## Author
akash k s

## Purpose
Academic Mini Project
