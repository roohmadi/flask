import psycopg2

class ExpenseTracker:
    def __init__(self, initial_balance=0):
        self.setup_database()
        self.initial_balance = initial_balance

    def get_connection(self):
        connection = psycopg2.connect(
            dbname="test",
            user="postgres",
            password="",
            host="localhost",
            port="5432"
        )
        return connection

    def setup_database(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id SERIAL PRIMARY KEY,
                        expense_date DATE,
                        category TEXT,
                        description TEXT,
                        amount REAL)''')
        conn.commit()
        cur.close()
        conn.close()

    def get_expenses(self):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        cur.close()
        conn.close()
        return expenses

    def add_expense(self, expense_date, category, description, amount):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (expense_date, category, description, amount) VALUES (%s, %s, %s, %s)", (expense_date, category, description, amount))
        conn.commit()
        cur.close()
        conn.close()

    def get_monthly_expense_total(self, year, month):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT SUM(amount) FROM expenses WHERE EXTRACT(YEAR FROM expense_date) = %s AND EXTRACT(MONTH FROM expense_date) = %s", (year, month))
        total = cur.fetchone()[0]
        cur.close()
        conn.close()
        return total if total else 0
    
    def delete_expense(self, expense_id):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        conn.commit()
        cur.close()
        conn.close()
        
    def set_initial_balance(self, initial_balance):
        self.initial_balance = initial_balance

    def get_initial_balance(self):
        return self.initial_balance