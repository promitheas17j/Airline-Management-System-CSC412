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

@app.route('/passenger/passenger_login', methods=['GET', 'POST'])
def passenger_login_page():
    if request.method == 'POST':
        entered_email = request.form.get('email')
        entered_password = request.form.get('password')

        try:
            record = search_passenger(entered_email)
        except:
            flash("User does not exist")
        else:
            if record[3] == entered_email:
                if record[4] == entered_password:
                    session['logged_in_user'] = record
                    session['logged_in_user_role'] = "passenger"
                    return redirect(url_for("home"))
                else:
                    flash("Email or password incorrect")
            else:
                flash("Email or password incorrect")

    return render_template("passenger/passenger_login.html")

@app.route('/admin/admin_login', methods=['GET', 'POST'])
def admin_login_page():
    if request.method == 'POST':
        entered_email = request.form.get('email')
        entered_password = request.form.get('password')

        try:
            record = search_admin(entered_email)
            print(record)
        except:
            flash("User does not exist")
        else:
            if record[3] == entered_email:
                if record[4] == entered_password:
                    session['logged_in_user'] = record
                    session['logged_in_user_role'] = "admin"
                    return redirect(url_for("home"))
                else:
                    flash("Email or password incorrect")
            else:
                flash("Email or password incorrect")

    return render_template("admin/admin_login.html")

# @app.route('/admin/admin_login')
# def admin_login_page():
#     return render_template("admin/admin_login.html")

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

def search_passenger(query):
    conn = get_db_connection()
    c = conn.cursor()

    temp = c.execute("SELECT * FROM passengers WHERE passenger_email LIKE ?", (query,)).fetchall()
    results = (temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5])

    conn.close()

    return results

def search_admin(query):
    conn = get_db_connection()
    c = conn.cursor()

    temp = c.execute("SELECT * FROM admins WHERE admin_email LIKE ?", (query,)).fetchall()
    results = (temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5])

    conn.close()

    return results

# def search_flights(departure_airport, arrival_airport, departure_date=None):
#     conn = get_db_connection()
#     c = conn.cursor()

#     if departure_date is None:
#         query = """
#             SELECT *
#             FROM flights
#             WHERE depart_loc = ? AND arrive_loc = ?
#         """
#         c.execute(query, (departure_airport, arrival_airport,))
#     else:
#         query = """
#             SELECT *
#             FROM flights
#             WHERE depart_loc = ? AND arrive_loc = ? AND depart_date = ?
#         """
#         c.execute(query, (departure_airport, arrival_airport, departure_date,))

#     matching_flights = c.fetchall()
#     for flight in matching_flights:
#         print("Flight[0] from DATE: " + str(flight[0]))

#     conn.close()
#     return matching_flights

# def search_flights(departure_airport, arrival_airport, departure_date):
#     conn = get_db_connection()
#     c = conn.cursor()

#     query = """
#         SELECT *
#         FROM flights
#         WHERE depart_loc = ? AND arrive_loc = ? AND depart_date = ?
#     """
#     c.execute(query, (departure_airport, arrival_airport, departure_date,))
#     matching_flights = c.fetchall()
#     for flight in matching_flights:
#         print("Flight[0] from DATE: " + str(flight[0]))

#     conn.close()
#     return matching_flights


def search_flights(departure_airport, arrival_airport):
    conn = get_db_connection()
    c = conn.cursor()

    query = """
        SELECT *
        FROM flights
        WHERE depart_loc = ? AND arrive_loc = ?
    """
    c.execute(query, (departure_airport, arrival_airport))
    matching_flights = c.fetchall()

    conn.close()
    return matching_flights


@app.route('/admin/admin_search_passengers')
def admin_search_passengers():
    return render_template("admin/admin_search_passengers.html")

@app.route('/admin/admin_passenger_results', methods=['GET', 'POST'])
def admin_passenger_results():
    query = request.form.get('search_email')
    if not search_passenger(query):
        flash("Message")
        return render_template("admin/admin_search_passengers.html")
    else:
        results = search_passenger(query)

    if results:
        session['passenger_result'] = results
        return render_template('admin/admin_passenger_results.html', query=query, results=results)
    elif not results:
        flash("No passenger account exists with email address " + str(query))
        print("No passenger account found")

    return render_template("admin/admin_search_passengers.html")

@app.route('/admin/admin_reset_password', methods=['GET', 'POST'])
def admin_reset_password():
    passenger = session.get('passenger_result')

    if request.method == 'POST':
        new_pass = request.form.get('new_password')

        conn = get_db_connection()
        conn.execute("UPDATE passengers SET password = ? WHERE passenger_id = ?", (new_pass, passenger[0],))

        conn.commit()
        conn.close()

    return render_template("admin/admin_reset_password.html")

@app.route('/admin/admin_delete_account', methods=['GET', 'POST'])
def admin_delete_account():
    passenger = session.get('passenger_result')

    if request.method == 'POST':
        confirmation = request.form.get('confirm_delete')

        if confirmation == "DELETE":
            conn = get_db_connection()
            conn.execute("DELETE FROM passengers WHERE passenger_id = ?", (passenger[0],))
            conn.commit()
            conn.close()

            return render_template("admin/admin_search_passengers.html")
    return render_template("admin/admin_delete_account.html")

@app.route('/passenger/edit_info', methods=['GET', 'POST'])
def passenger_edit_info():
    passenger_id = session.get("logged_in_user")[0]

    if request.method == 'POST':
        entered_email = request.form.get("email")
        entered_password = request.form.get("password")
        entered_passport_no = request.form.get("passport_no")

        conn = get_db_connection()
        if entered_email:
            conn.execute("UPDATE passengers SET passenger_email = ? WHERE passenger_id = ?", (entered_email, passenger_id,))
            conn.commit()
        if entered_password:
            conn.execute("UPDATE passengers SET password = ? WHERE passenger_id = ?", (entered_password, passenger_id,))
            conn.commit()
        if entered_passport_no:
            conn.execute("UPDATE passengers SET passport_no = ? WHERE passenger_id = ?", (entered_passport_no, passenger_id,))
            conn.commit()

        conn.close()
    return render_template("passenger/edit_info.html")

@app.route('/passenger/passenger_search_flights', methods=['GET', 'POST'])
def passenger_search_flights():
    if request.method == 'POST':
        session['departure_airport'] = request.form.get("departure-loc")
        session['arrival_airport'] = request.form.get("arrival-loc")
        session['departure_date'] = request.form.get("departure-date")

        return redirect(url_for("passenger_flight_results"))
    return render_template("passenger/passenger_search_flights.html")

@app.route('/passenger/passenger_flight_results', methods=['GET', 'POST'])
def passenger_flight_results():
    session['reserved'] = "None"
    departure_airport = session.get('departure_airport')
    arrival_airport = session.get('arrival_airport')

    user_role = session.get("logged_in_user_role")

    flights = search_flights(departure_airport, arrival_airport)

    if request.method == "POST":
        if user_role == "passenger":
            flight_number = request.form.get('flight_number')
            passenger_id = session.get("logged_in_user")[0]
            session['reserved'] = "True"
        else:
            session['reserved'] = "False"

    reservation_status = session.get('reserved')
    print(reservation_status)
    if reservation_status == "True":
        conn = get_db_connection()
        c = conn.cursor()

        c.execute("SELECT * FROM reservations WHERE passenger_id = ? AND flight_no = ?", (passenger_id, flight_number))
        existing_reservation = c.fetchone()
        if existing_reservation:
            flash("Reservation already exists")
        else:
            c.execute("INSERT INTO reservations (passenger_id, flight_no) VALUES (?, ?)", (passenger_id, flight_number))
            conn.commit()
            flash("Reservation successful")
    else:
        if reservation_status == "False":
            flash("You can't do that")

    return render_template("passenger/flight_results.html", flights=flights)

@app.route('/notready')
def not_ready_page():
    return render_template("not_built_yet.html")

if __name__ == "__main__":
    app.run(debug=True)
