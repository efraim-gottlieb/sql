import mysql.connector
from mysql.connector import Error 

class EmployeeDB:
    def __init__(self, host, user, password, datebase):
      self.host = host
      self.user = user
      self.password = password
      self.database = datebase

    def connect(self):
      try:
        self.DB = mysql.connector.connect(
        host = self.host,
        user = self.user,
        password = self.password,
        database = self.database)
        if self.DB.is_connected():
          print("✅ Connection to MySQL DB successful")
      except:
        print(Error('Connection failed'))

    def create_employees_table(self):
      cursor = self.DB.cursor()
      cursor.execute("""
                     CREATE TABLE IF NOT EXISTS employees(
                     id INT AUTO_INCREMENT,
                     name VARCHAR(100) NOT NULL,
                     department VARCHAR(50),
                     salary DECIMAL(10,2),
                     PRIMARY KEY (id)
                     );
                      """)
      self.DB.commit()
      print('✅ Table ready')
      cursor.close()

    def add_employee(self, name, department, salary):
      cursor = self.DB.cursor()
      cursor.execute('INSERT INTO employees (name, department, salary) VALUES ' +
      f"('{name}', '{department}', '{salary}');")
      self.DB.commit()
      print(f'✅ added {name} ID: {cursor.lastrowid}')
      cursor.close()

    def get_all_employees(self):
      cursor = self.DB.cursor()
      cursor.execute('SELECT * FROM employees')
      rows = cursor.fetchall()
      rows = [{'id':row[0], 'name':row[1], 'department': row[2], 'salary':float(row[3])} for row in rows]
      if rows:
        return rows
      else:
        print('not rows!')
      cursor.close()

    def get_employee_by_id(self, id):
      cursor = self.DB.cursor()
      cursor.execute(f'SELECT * FROM employees WHERE id = {id}')
      row = cursor.fetchone()
      cursor.close()
      if row:
        return {'id':row[0], 'name':row[1], 'department': row[2], 'salary':float(row[3])}
      else:
        return None
      
    def update_salary(self, emp_id, new_salary):
      cursor = self.DB.cursor()
      cursor.execute(f'UPDATE employees SET salary = {new_salary} WHERE id = {emp_id}')
      self.DB.commit()
      cursor.close()
      print('✅ salary updated!')



a = EmployeeDB('localhost', 'root', 'root', 'employeesdb')

a.connect()
print(a.get_employee_by_id(4))



