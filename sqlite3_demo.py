import sqlite3
from employee import Employee
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE employees (
          first text,
          last text,
          pay integer
)""")
# CRUD tactics
def insert_emp(emp):
    with conn:
        query = "INSERT INTO employees VALUES (:first, :last, :pay)"
        values = {'first': emp.first, 'last': emp.last, 'pay': emp.pay}
        print("Insert Query:", query)
        print("Insert Values:", values)
        c.execute(query, values)
def get_emps_by_name(lastname):
    query = "SELECT * FROM employees WHERE last=:last"
    values = {'last': lastname}
    print("Select Query:", query)
    print("Select Values:", values)
    c.execute(query, values)
    return c.fetchall()
def update_pay(emp, pay):
    with conn:
        query = """UPDATE employees SET pay = :pay
                  WHERE first = :first AND last = :last"""
        values = {'first': emp.first, 'last': emp.last, 'pay': pay}
        print("Update Query:", query)
        print("Update Values:", values)
        c.execute(query, values)
def remove_emp(emp):
    with conn:
        query = "DELETE from employees WHERE first = :first AND last = :last"
        values = {'first': emp.first, 'last': emp.last}
        print("Delete Query:", query)
        print("Delete Values:", values)
        c.execute(query, values)
emp_1 = Employee('John', 'Doe', 80000)
emp_2 = Employee('Jane', 'Doe', 90000)
insert_emp(emp_1)
insert_emp(emp_2)
emps = get_emps_by_name('Doe')
print("Employees:", emps)
update_pay(emp_2, 95000)
remove_emp(emp_1)
conn.close()