from flask import Flask, render_template, request, url_for, flash, redirect, session
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

# def perform_search(query, query_field):
#     conn = get_db_connection()
#     c = conn.cursor()

#     if query_field == "pemail":
#         results = c.execute("SELECT * FROM passengers WHERE passenger_email LIKE ?", (query,)).fetchall()
#     elif query_field == "pid":
#         results = c.execute("SELECT * FROM passengers WHERE passenger_id LIKE ?", (query,)).fetchall()
#     else:
#         results = "Empty"

#     conn.close()

#     return results

def perform_search(query):
    conn = get_db_connection()
    c = conn.cursor()

    temp = c.execute("SELECT * FROM passengers WHERE passenger_email LIKE ?", (query,)).fetchall()
    results = (temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5])

    conn.close()

    return results

@app.route('/admin_search_passengers')
def admin_search_passengers():
    return render_template("admin_search_passengers.html")

@app.route('/admin_results_passengers', methods=['GET', 'POST'])
def admin_results_passengers():
    query = request.form.get('search_email')
    results = perform_search(query)

    session['passenger_result'] = results

    # TODO: Move reset password functionality to its own endpoint using sessions
    if request.method == 'POST':
        conn = get_db_connection()

        new_pass = request.form.get('new_pass')
        print("new_pass " + str(new_pass))
    #     conn.execute('UPDATE passengers SET password = ? WHERE passenger_email=?;', (new_pass, results[0][3],))
    #     print(new_pass)
    #     print(conn.execute("SELECT * FROM passengers WHERE passenger_email LIKE ?", (results,)).fetchall())

    #     conn.close()

    return render_template('admin_passenger_results.html', query=query, results=results)

@app.route('/notready')
def not_ready_page():
    return render_template("not_built_yet.html")

if __name__ == "__main__":
    app.run(debug=True)
