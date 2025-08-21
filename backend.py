import psycopg2
from psycopg2 import sql

# --- Database Configuration ---
DB_HOST = "localhost"
DB_NAME = "hr_project"
DB_USER = "postgres"
DB_PASSWORD = "suhani.."
DB_PORT = 5432

def get_db_connection():
    """Establishes and returns a new database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# --- CRUD Operations ---

def create_employee(employee_id, first_name, last_name, department, hire_date, salary):
    """Inserts a new employee into the database."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO employees (employee_id, first_name, last_name, department, hire_date, salary) VALUES (%s, %s, %s, %s, %s, %s)",
                    (employee_id, first_name, last_name, department, hire_date, salary)
                )
                conn.commit()
                return True
            except psycopg2.Error as e:
                print(f"Error creating employee: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()

def read_employees(department_filter=None, sort_by=None):
    """Retrieves a list of all employees, with optional filtering and sorting."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            try:
                query = "SELECT employee_id, first_name, last_name, department, hire_date, salary FROM employees"
                params = []
                
                if department_filter and department_filter != "All":
                    query += " WHERE department = %s"
                    params.append(department_filter)
                
                if sort_by == 'salary':
                    query += " ORDER BY salary DESC"
                elif sort_by == 'hire_date':
                    query += " ORDER BY hire_date DESC"
                
                cur.execute(query, params)
                return cur.fetchall()
            except psycopg2.Error as e:
                print(f"Error reading employees: {e}")
                return []
            finally:
                conn.close()

def update_employee(employee_id, first_name, last_name, department, hire_date, salary):
    """Updates an existing employee's information."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE employees SET first_name = %s, last_name = %s, department = %s, hire_date = %s, salary = %s WHERE employee_id = %s",
                    (first_name, last_name, department, hire_date, salary, employee_id)
                )
                conn.commit()
                return True
            except psycopg2.Error as e:
                print(f"Error updating employee: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()

def delete_employee(employee_id):
    """Deletes an employee from the database."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
                conn.commit()
                return True
            except psycopg2.Error as e:
                print(f"Error deleting employee: {e}")
                conn.rollback()
                return False
            finally:
                conn.close()

# --- Analytics Functions ---

def get_employee_departments():
    """Returns a list of all unique departments."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT DISTINCT department FROM employees ORDER BY department")
                departments = [row[0] for row in cur.fetchall()]
                return departments
            except psycopg2.Error as e:
                print(f"Error getting departments: {e}")
                return []
            finally:
                conn.close()

def get_total_employees():
    """Returns the total number of employees."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM employees")
            result = cur.fetchone()
            return result[0] if result else 0
        conn.close()

def get_total_salary_sum():
    """Returns the sum of all employee salaries."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(salary) FROM employees")
            result = cur.fetchone()
            return result[0] if result else 0
        conn.close()

def get_average_salary():
    """Returns the average employee salary."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM employees")
            result = cur.fetchone()
            return result[0] if result else 0
        conn.close()

def get_min_salary():
    """Returns the lowest employee salary."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MIN(salary) FROM employees")
            result = cur.fetchone()
            return result[0] if result else 0
        conn.close()

def get_max_salary():
    """Returns the highest employee salary."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT MAX(salary) FROM employees")
            result = cur.fetchone()
            return result[0] if result else 0
        conn.close()

def get_department_salary_summary():
    """Returns department-wise salary summary (avg, min, max)."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            query = "SELECT department, AVG(salary), MIN(salary), MAX(salary) FROM employees GROUP BY department"
            cur.execute(query)
            return cur.fetchall()
        conn.close()
