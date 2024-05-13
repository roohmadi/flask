from flask import Flask, render_template, request, redirect, url_for
from expense_tracker import ExpenseTracker

app = Flask(__name__)
expense_tracker = ExpenseTracker()

@app.route('/')
def index():
    expenses = expense_tracker.get_expenses()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add():
    expense_date = request.form['date']
    category = request.form['category']
    description = request.form['description']
    amount = request.form['amount']
    expense_tracker.add_expense(expense_date, category, description, amount)
    expenses = expense_tracker.get_expenses()
    return render_template('index.html', expenses=expenses)

# Rute untuk menampilkan jumlah pengeluaran bulanan
@app.route('/monthly_expense', methods=['GET'])
def monthly_expense():
    year = request.args.get('year')
    month = request.args.get('month')
    if year and month:
        total = expense_tracker.get_monthly_expense_total(int(year), int(month))
        return f"Total pengeluaran bulan {month} tahun {year} adalah: {total}"
    else:
        return "Tahun dan bulan harus disertakan dalam parameter query."

@app.route('/set_initial_balance', methods=['GET', 'POST'])
def set_initial_balance():
    if request.method == 'POST':
        initial_balance = float(request.form['initial_balance'])
        expense_tracker.set_initial_balance(initial_balance)
        return redirect(url_for('index'))
    return render_template('set_initial_balance.html')

@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    # Ambil ID pengeluaran dari form
    expense_id = int(request.form['expense_id'])
    
    # Hapus pengeluaran dari database berdasarkan ID
    expense_tracker.delete_expense(expense_id)
    
    # Redirect kembali ke halaman utama
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)