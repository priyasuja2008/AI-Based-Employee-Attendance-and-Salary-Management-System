from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "attendance_secret_key"

# ---------------- DATABASE CONNECTION ---------------- #

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Priya123@",   # Replace with your MySQL password
        database="attendance_system"
    )

# -----------------signup------------------#
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if an admin already exists
    cursor.execute("SELECT * FROM users WHERE role='admin'")
    admin = cursor.fetchone()

    if admin:
        cursor.close()
        conn.close()
        flash("Admin account already exists. Please login.")
        return redirect(url_for('login'))

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # 👇 ADD THE USERNAME CHECK HERE
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists. Please choose another username.")
            cursor.close()
            conn.close()
            return redirect(url_for('signup'))

        # Password check
        if password != confirm_password:
            flash("Passwords do not match.")
            cursor.close()
            conn.close()
            return redirect(url_for('signup'))

        # Insert new admin
        cursor.execute("""
            INSERT INTO users(username,email,password,role)
            VALUES(%s,%s,%s,%s)
        """, (username, email, password, "admin"))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Admin account created successfully!")
        return redirect(url_for('login'))

    cursor.close()
    conn.close()

    return render_template("signup.html")
# ---------------- LOGIN ---------------- #

@app.route('/')
def home():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE role='admin'")
    admin = cursor.fetchone()

    cursor.close()
    conn.close()

    if admin:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('signup'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Username or Password")

    return render_template("login.html")

# ---------------- DASHBOARD ---------------- #

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM employees")
    total_employees = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_employees=total_employees
    )
# ---------------- EMPLOYEES ---------------- #

@app.route('/employees')
def employees():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            emp_id,
            employee_code,
            name,
            gender,
            phone,
            email,
            designation
        FROM employees
        ORDER BY emp_id
    """)

    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("employees.html", employees=employees)
# ---------------- REGISTER EMPLOYEE ---------------- #

@app.route('/register_employee', methods=['GET', 'POST'])
def register_employee():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        employee_id = request.form['employee_id']
        full_name = request.form['full_name']
        gender = request.form['gender']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        department = request.form['department']
        designation = request.form['designation']
        joining_date = request.form['joining_date']
        shift = request.form['shift']
        salary = request.form['salary']
        status = request.form['status']

        cursor.execute("""
        INSERT INTO employees
        (employee_id,full_name,gender,dob,email,phone,address,
        department,designation,joining_date,shift,salary,status)

        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,(employee_id,full_name,gender,dob,email,phone,address,
             department,designation,joining_date,shift,salary,status))

        conn.commit()

        flash("Employee Registered Successfully")

        cursor.close()
        conn.close()

        return redirect(url_for("employees"))

    cursor.execute("SELECT COUNT(*) AS total FROM employees")
    total = cursor.fetchone()['total'] + 1

    employee_id = f"EMP{total:03}"

    cursor.close()
    conn.close()

    return render_template(
        "register_employee.html",
        employee_id=employee_id
    )

# ---------------- ATTENDANCE ---------------- #

@app.route('/attendance')
def attendance():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template("attendance.html")

# ---------------- ATTENDANCE HISTORY ---------------- #

@app.route('/attendance_history')
def attendance_history():

    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM attendance ORDER BY attendance_date DESC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("attendance_history.html", data=data)

# ---------------- REPORTS ---------------- #

@app.route('/reports')
def reports():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template("reports.html")

# ---------------- SALARY ---------------- #

@app.route('/salary')
def salary():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template("salary.html")

# ---------------- CAMERA ---------------- #

@app.route('/camera')
def camera():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template("camera.html")

# ---------------- LOGOUT ---------------- #

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)                                                                                                         