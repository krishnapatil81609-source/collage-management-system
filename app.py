from flask import Flask, render_template, request, redirect
import sqlite3
from flask_mail import Mail, Message
app = Flask(__name__)


# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'krishnapatil81609@gmail.com'

# Yaha Gmail App Password dalna
app.config['MAIL_PASSWORD'] = 'nuxhsboogyqqtmta'

mail = Mail(app)



@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        msg = Message(
            subject=f"New Message from {name}",
            sender="krishnapatil81609@gmail.com",
            recipients=["krishnapatil81609@gmail.com"]
        )

        msg.body = f"""
Name: {name}
Email: {email}

Message:
{message}
"""

        mail.send(msg)

        return redirect("/dashboard")

    return render_template("dashbord.html")


#========================================================================================
def create_table():
    conn = sqlite3.connect("database/student.db")
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   student_id TEXT,
                   name TEXT,
                   age INTEGER,
                   cource TEXT
                   )
                   """)
    conn.commit()
    conn.close()

create_table()
#=====================================================================================================
@app.route("/",methods = ["POST","GET"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/student.db")
        cursor = conn.cursor()
        
        cursor.execute("""
SELECT * FROM register WHERE username = ? AND password = ? 
                       """,(username,password))
        
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect("/dashboard")
        else:
            return "username or password not found"
        
    return render_template("login.html")

#======================================================================================================
@app.route("/add_student",methods=["POST","GET"])
def add_student():
    if request.method == "POST" :
        student_id = request.form["student_id"]
        name = request.form["name"]
        age = request.form["age"]
        cource = request.form["cource"]

        
        conn = sqlite3.connect("database/student.db")
        cursor = conn.cursor()
        cursor.execute("""
INSERT INTO students(student_id,name,age,cource) VALUES (?,?,?,?)
                       """,
                       (student_id,name,age,cource))
        
        
        
        conn.commit()
        conn.close()

        return redirect("/")


    return render_template("addstudent.html")

#==========================================================================================================
@app.route("/student_view")
def view_student():

    coon = sqlite3.connect("database/student.db")
    cursor = coon.cursor()
    cursor.execute("""
SELECT * FROM students
                   """)
    
    students = cursor.fetchall()

    
    coon.close()
    
    
    return render_template("viewstudent.html",students=students)

#==========================================================================================================
@app.route("/delete", methods=["POST","GET"])
def delete_student():
    if request.method == "POST":
        student_id = request.form["student_id"]

        conn = sqlite3.connect("database/student.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        student = cursor.fetchone()

        if student:
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            conn.commit()
            conn.close()
            return redirect("/dashboard")
        else:
            conn.close()
            return "account not found"

    return render_template("delete.html")

    
#==========================================================================================================
@app.route("/dashboard", methods=["POST","GET"])
def dashbord():
    conn = sqlite3.connect("database/student.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]  # yeh number dega jaise 5, 10
    conn.close()
    
    return render_template("dashbord.html", total_students=total)
    

#==========================================================================================================
def create_table():
    conn = sqlite3.connect("database/student.db")
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS register(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   password TEXT,
                   mobile INTEGER
                   )
                   """)
    conn.commit()
    conn.close()

create_table()
#==========================================================================================================
@app.route("/register", methods = ["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = sqlite3.connect("database/student.db")
        cursor = conn.cursor()
        cursor.execute("""
INSERT INTO register(username,password,mobile) VALUES (?,?,?)
                       """,
                       (username,password,mobile))
        
        
        
        conn.commit()
        conn.close()

        return redirect("/")


    return render_template("register.html")
























































































if __name__ == "__main__":
    app.run(debug=True)