from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import redirect
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

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/signup', methods=('GET', 'POST'))
def signup_page():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()

    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        if not fname:
            flash('First name is required!')
        elif not lname:
            flash('Last name is required!')
        elif not email:
            flash('Email is required!')
        elif not password:
            flash('Password is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (fname, lname, email, password) VALUES (?, ?, ?, ?)',
                         (fname, lname, email, password)
            )
            conn.commit()
            conn.close()

            return redirect(url_for('home'))

    return render_template("signup.html", users=users)

@app.route('/notready')
def not_ready_page():
    return render_template("not_built_yet.html")

if __name__ == "__main__":
    app.run(debug=True)
