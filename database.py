import sqlite3

conn = sqlite3.connect('attendance_system') 
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    employee_id TEXT UNIQUE,
    department TEXT,
    position TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    date TEXT,
    check_in TEXT,
    check_out TEXT,
    status TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS salary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    month TEXT,
    basic_salary REAL,
    days_present INTEGER,
    total_salary REAL
)
''')

conn.commit()
conn.close()

print("Database created successfully!")