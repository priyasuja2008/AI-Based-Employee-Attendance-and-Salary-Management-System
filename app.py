from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/employees')
def employees():
    return render_template('employees.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/salary')
def salary():
    return render_template('salary.html')

if __name__ == '__main__':
    app.run(debug=True)