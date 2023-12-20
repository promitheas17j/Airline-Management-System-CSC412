from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

db_file_name = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(db_file_name)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.debug = True

@app.route('/')
def home():
    conn = get_db_connection()
    flights = conn.execute("SELECT * FROM flights").fetchall()
    conn.close()

    return render_template("index.html", flights=flights)

@app.route('/passenger_login')
def passenger_login_page():
    return render_template("passenger_login.html")

@app.route('/admin_login')
def admin_login_page():
    return render_template("admin_login.html")

@app.route('/signup', methods=('GET', 'POST'))
def signup_page():
    conn = get_db_connection()
    passengers = conn.execute("SELECT * FROM passengers").fetchall()
    admins = conn.execute("SELECT * FROM admins").fetchall()
    conn.close()

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        passenger_email = request.form['passenger_email']
        password = request.form['password']

        if not fname:
            flash('First name is required!')
        elif not lname:
            flash('Last name is required!')
        elif not passenger_email:
            flash('Email is required!')
        elif not password:
            flash('Password is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO passengers (fname, lname, passenger_email, password) VALUES (?, ?, ?, ?)',
                         (fname, lname, passenger_email, password)
            )
            conn.commit()
            conn.close()

            return redirect(url_for('home'))

    return render_template("signup.html", passengers=passengers, admins=admins)

def perform_search(query):
    conn = get_db_connection()
    c = conn.cursor()

    results = c.execute("SELECT * FROM passengers WHERE passenger_email LIKE ?", (query,)).fetchall()

    conn.close()

    return results

@app.route('/admin_search_passengers')
def admin_search_passengers():
    return render_template("admin_search_passengers.html")

@app.route('/admin_results_passengers', methods=['POST'])
def admin_results_passengers():
    query = request.form.get('passenger_email')
    results = perform_search(query)

    return render_template('admin_passenger_results.html', query=query, results=results)

@app.route('/notready')
def not_ready_page():
    return render_template("not_built_yet.html")

if __name__ == "__main__":
    app.run(debug=True)
