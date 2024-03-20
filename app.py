from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
from employee import Employee
app = Flask(__name__)
# Function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect('employee.db')
    conn.row_factory = sqlite3.Row
    return conn
# Function to get database connection for each request
def get_db():
    with app.app_context():
        db = getattr(g, '_database', None)
        if db is None:
            g._database = sqlite3.connect('employee.db')
            g._database.row_factory = sqlite3.Row
        return g._database
# Create table if not exists (moved inside a function)
def create_table():
    conn = get_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS employees (
              id INTEGER PRIMARY KEY,
              first TEXT,
              last TEXT,
              pay INTEGER
    )""")
    conn.commit()
# CRUD operations
def insert_emp(emp):
    conn = get_db()
    with conn:
        c = conn.cursor()
        c.execute("INSERT INTO employees VALUES (NULL, ?, ?, ?)", (emp.first, emp.last, emp.pay))
def get_emps_by_name(lastname):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE last=?", (lastname,))
    return c.fetchall()
def update_pay(emp_id, pay):
    conn = get_db()
    with conn:
        c = conn.cursor()
        c.execute("UPDATE employees SET pay = ? WHERE id = ?", (pay, emp_id))
def remove_emp(emp_id):
    conn = get_db()
    with conn:
        c = conn.cursor()
        c.execute("DELETE from employees WHERE id = ?", (emp_id,))
# Ensure table creation before running the app
create_table()
# Routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/add', methods=['POST'])
def add_employee():
    first = request.form['first']
    last = request.form['last']
    # pay = int(request.form['pay'])
    pay = float(request.form['pay'])  # Convert the input to a float instead of an int
    emp = Employee(first, last, pay)
    insert_emp(emp)
    return redirect(url_for('index'))
@app.route('/search', methods=['POST'])
def search_employee():
    lastname = request.form['lastname']
    emps = get_emps_by_name(lastname)
    return render_template('index.html', emps=emps)
@app.route('/update', methods=['POST'])
def update_employee():
    emp_id = request.form['id']
    pay = int(request.form['pay'])
    update_pay(emp_id, pay)
    return redirect(url_for('index'))
@app.route('/delete', methods=['POST'])
def delete_employee():
    emp_id = request.form['id']
    remove_emp(emp_id)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)