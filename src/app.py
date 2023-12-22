from flask import Flask, render_template, request, url_for, flash, redirect, session
import sqlite3
import util_functions

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.debug = True


@app.route('/')
def home():
    conn = util_functions.get_db_connection()
    flights = conn.execute("SELECT * FROM flights").fetchall()
    conn.close()

    return render_template("index.html", flights=flights, role=util_functions.get_logged_in_user_role())


@app.route("/logout")
def logout():
    util_functions.set_logged_in_role("None")
    return redirect(url_for("home"))


@app.route('/passenger/login', methods=['GET', 'POST'])
def passenger_login_page():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "None":
        return redirect(url_for("home"))

    if request.method == 'POST':
        entered_email = request.form.get('email')
        entered_password = request.form.get('password')

        try:
            record = util_functions.search_passenger(entered_email)
        except:
            flash("User does not exist")
        else:
            if record[3] == entered_email:
                if record[4] == entered_password:
                    util_functions.set_logged_in_user_record(record)
                    util_functions.set_logged_in_role("passenger")
                    return redirect(url_for("home"))
                else:
                    flash("Email or password incorrect")
            else:
                flash("Email or password incorrect")
    return render_template("passenger/login.html", role=util_functions.get_logged_in_user_role())


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_page():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "None":
        return redirect(url_for("home"))

    if request.method == 'POST':
        entered_email = request.form.get('email')
        entered_password = request.form.get('password')

        try:
            record = util_functions.search_admin(entered_email)
        except:
            flash("User does not exist")
        else:
            if record[3] == entered_email:
                if record[4] == entered_password:
                    # session['logged_in_user'] = record
                    # session['logged_in_user_role'] = "admin"
                    util_functions.set_logged_in_user_record(record)
                    util_functions.set_logged_in_role("admin")
                    return redirect(url_for("home"))
                else:
                    flash("Email or password incorrect")
            else:
                flash("Email or password incorrect")
    return render_template("admin/login.html", role=util_functions.get_logged_in_user_role())


@app.route('/signup', methods=('GET', 'POST'))
def signup_page():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "None":
        return redirect(url_for("home"))

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
            conn = util_functions.get_db_connection()
            conn.execute('INSERT INTO passengers (fname, lname, passenger_email, password) VALUES (?, ?, ?, ?)', (fname, lname, passenger_email, password))
            conn.commit()
            conn.close()

            return redirect(url_for('home'))
    return render_template("signup.html", role=util_functions.get_logged_in_user_role())


@app.route('/admin/search_passengers')
def admin_search_passengers():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "admin":
        return redirect(url_for("home"))

    return render_template("admin/search_passengers.html", role=util_functions.get_logged_in_user_role())


@app.route('/admin/passenger_results', methods=['GET', 'POST'])
def admin_passenger_results():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "admin":
        return redirect(url_for("home"))

    query = request.form.get('search_email')
    results = util_functions.search_passenger(query)
    # if not util_functions.search_passenger(query):
    if not results:
        flash("User not found")
        return render_template("admin/search_passengers.html", role=util_functions.get_logged_in_user_role())
    else:
        results = util_functions.search_passenger(query)

    if results:
        session['passenger_result'] = results
        return render_template('admin/passenger_results.html', query=query, results=results, role=util_functions.get_logged_in_user_role())
    elif not results:
        flash("No passenger account exists with email address " + str(query))
    return render_template("admin/search_passengers.html", role=util_functions.get_logged_in_user_role())


@app.route('/admin/reset_password', methods=['GET', 'POST'])
def admin_reset_password():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "admin":
        return redirect(url_for("home"))

    passenger = session.get('passenger_result')

    if request.method == 'POST':
        new_pass = request.form.get('new_password')

        conn = util_functions.get_db_connection()
        conn.execute("UPDATE passengers SET password = ? WHERE passenger_id = ?", (new_pass, passenger[0],))
        conn.commit()
        conn.close()
    return render_template("admin/reset_password.html", role=util_functions.get_logged_in_user_role())


@app.route('/admin/delete_account', methods=['GET', 'POST'])
def admin_delete_account():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "admin":
        return redirect(url_for("home"))

    passenger = session.get('passenger_result')

    if request.method == 'POST':
        confirmation = request.form.get('confirm_delete')

        if confirmation == "DELETE":
            conn = util_functions.get_db_connection()
            conn.execute("DELETE FROM passengers WHERE passenger_id = ?", (passenger[0],))
            conn.commit()
            conn.close()

            return render_template("admin/search_passengers.html", role=util_functions.get_logged_in_user_role())
    return render_template("admin/delete_account.html", role=util_functions.get_logged_in_user_role())


@app.route("/admin/manage_flights", methods=["GET", "POST"])
def admin_manage_flights():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "admin":
        return redirect(url_for("home"))

    all_flights = util_functions.get_available_flights(None)
    return render_template("admin/manage_flights.html", flights=all_flights, role=util_functions.get_logged_in_user_role())


@app.route('/admin/edit_flight/<flight_number>', methods=['GET', 'POST'])
def admin_edit_flight(flight_number):
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "admin":
        return redirect(url_for("home"))

    conn = util_functions.get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM flights WHERE flight_no = ?", (flight_number,))
    flight = c.fetchone()
    conn.close()

    if request.method == 'POST':
        depart_loc = request.form.get("depart_loc")
        arrive_loc = request.form.get("arrive_loc")
        depart_date = request.form.get("depart_date")
        depart_time = request.form.get("depart_time")

        conn = util_functions.get_db_connection()
        if depart_loc:
            conn.execute("UPDATE flights SET depart_loc = ? WHERE flight_no = ?", (depart_loc, flight_number,))
            conn.commit()
        if arrive_loc:
            conn.execute("UPDATE flights SET arrive_loc = ? WHERE flight_no = ?", (arrive_loc, flight_number,))
            conn.commit()
        if depart_date:
            conn.execute("UPDATE flights SET depart_date = ? WHERE flight_no = ?", (depart_date, flight_number,))
            conn.commit()
        if depart_time:
            conn.execute("UPDATE flights SET depart_time = ? WHERE flight_no = ?", (depart_time, flight_number,))
            conn.commit()
        conn.close()
    return render_template("admin/edit_flight.html", flight=flight, role=util_functions.get_logged_in_user_role())


@app.route("/admin/add_flight", methods=["GET", "POST"])
def admin_add_flight():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "admin":
        return redirect(url_for("home"))

    conn = util_functions.get_db_connection()
    c = conn.cursor()

    logged_in_user_role = util_functions.get_logged_in_user_role()

    if request.method == "POST":
        flight_number = request.form.get("flight_number")
        international = request.form.get("international")
        if international == "on":
            international = 1
        elif international == None:
            international = 0
        else:
            flash("Unknown value received for international checkbox. You should never see this message")

        depart_loc = request.form.get("depart_loc")
        arrive_loc = request.form.get("arrive_loc")
        depart_date = request.form.get("depart_date")
        depart_time = request.form.get("depart_time")
        depart_country = request.form.get("depart_country")
        arrive_country = request.form.get("arrive_country")

        c.execute("INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (flight_number, international, depart_loc, arrive_loc, depart_date, depart_time, depart_country, arrive_country))
        conn.commit()

        flash(f"Record for flight number: {flight_number} added!")
    conn.close()
    return render_template("admin/add_flight.html", role=util_functions.get_logged_in_user_role())

@app.route('/passenger/edit_info', methods=['GET', 'POST'])
def passenger_edit_info():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "passenger":
        return redirect(url_for("home"))

    passenger_id = util_functions.get_logged_in_passenger_id()

    if request.method == 'POST':
        entered_email = request.form.get("email")
        entered_password = request.form.get("password")
        entered_passport_no = request.form.get("passport_no")

        conn = util_functions.get_db_connection()
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
    return render_template("passenger/edit_info.html", role=util_functions.get_logged_in_user_role())


@app.route('/passenger/search_flights', methods=['GET', 'POST'])
def passenger_search_flights():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "passenger":
        return redirect(url_for("home"))

    if request.method == 'POST':
        session['departure_airport'] = request.form.get("departure-loc")
        session['arrival_airport'] = request.form.get("arrival-loc")
        session['departure_date'] = request.form.get("departure-date")

        return redirect(url_for("passenger_flight_results"))

    if logged_in_user_role == "passenger":
        passenger_id = util_functions.get_logged_in_passenger_id()

        if passenger_id is not None:
            available_flights = util_functions.get_available_flights(passenger_id)
        else:
            available_flights = util_functions.get_available_flights(None)
    return render_template("passenger/search_flights.html", available_flights=available_flights, role=util_functions.get_logged_in_user_role())


@app.route('/passenger/flight_results', methods=['GET', 'POST'])
def passenger_flight_results():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "passenger":
        return redirect(url_for("home"))

    util_functions.set_session_reservation_status("None")
    departure_airport = session.get('departure_airport')
    arrival_airport = session.get('arrival_airport')

    user_role = util_functions.get_logged_in_user_role()
    passenger_id = util_functions.get_logged_in_passenger_id()

    matching_flights = util_functions.search_flights(departure_airport, arrival_airport)

    if request.method == "POST":
        flight_number = request.form.get("flight_number")
        reservation_status = util_functions.check_reservation_status(passenger_id, flight_number)
        if user_role == "passenger":
            flight_number = request.form.get('flight_number')
            passenger_id = util_functions.get_logged_in_passenger_id()
            util_functions.set_session_reservation_status("True")
        else:
            util_functions.set_session_reservation_status("False")

        reservation_status = util_functions.get_session_reservation_status()
        if reservation_status == "True":
            conn = util_functions.get_db_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM reservations WHERE passenger_id = ? AND flight_no = ?", (passenger_id, flight_number))
            existing_reservation = c.fetchone()
            if existing_reservation:
                flash("Reservation already exists")
                return redirect(url_for("passenger_search_flights"))
            else:
                c.execute("INSERT INTO reservations (passenger_id, flight_no) VALUES (?, ?)", (passenger_id, flight_number))
                conn.commit()
                flash("Reservation successful")
                return redirect(url_for("passenger_search_flights"))
    return render_template("passenger/flight_results.html", flights=matching_flights, role=util_functions.get_logged_in_user_role())


@app.route('/passenger/view_reservations', methods=['GET', 'POST'])
def passenger_view_reservations():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "passenger":
        return redirect(url_for("home"))

    passenger_id = util_functions.get_logged_in_passenger_id()

    conn = util_functions.get_db_connection()
    c = conn.cursor()
    query = """
        SELECT f.*
        FROM flights f
        JOIN reservations r on f.flight_no = r.flight_no
        WHERE r.passenger_id = ?
    """
    c.execute(query, (passenger_id,))
    reservations = c.fetchall()

    if request.method == "POST":
        flight_number = request.form.get("flight_number")
        c.execute("SELECT * FROM reservations WHERE passenger_id = ? AND flight_no = ?", (passenger_id, flight_number,))
        reservation = c.fetchone()

        if reservation:
            c.execute("DELETE FROM reservations WHERE passenger_id = ? AND flight_no = ?", (passenger_id, flight_number,))
            conn.commit()
            flash("Reservation cancelled")
            return redirect(url_for("passenger_view_reservations"))
    return render_template("passenger/view_reservations.html", reservations=reservations, role=util_functions.get_logged_in_user_role())


@app.route('/passenger/view_cart', methods=['GET', 'POST'])
def passenger_view_cart():
    logged_in_user_role = util_functions.get_logged_in_user_role()
    if logged_in_user_role != "passenger":
        return redirect(url_for("home"))

    passenger_id = util_functions.get_logged_in_passenger_id()

    conn = util_functions.get_db_connection()
    c = conn.cursor()
    query = """
        SELECT f.*
        FROM flights f
        JOIN booked_flights b on f.flight_no = b.flight_no
        WHERE b.passenger_id = ?
    """
    c.execute(query, (passenger_id,))
    reservations = c.fetchall()

    if request.method == "POST":
        flight_number = request.form.get("flight_number")
        c.execute("SELECT * FROM reservations WHERE passenger_id = ? AND flight_no = ?", (passenger_id, flight_number,))
        reservation = c.fetchone()

        if reservation:
            # c.execute("DELETE FROM reservations WHERE passenger_id = ? AND flight_no = ?", (passenger_id, flight_number,))
            c.execute("INSERT INTO booked_flights VALUES (?, ?)", (passenger_id, flight_number,))
            conn.commit()
            flash(f"Payment for flight {flight_number} complete!")
            return redirect(url_for("passenger_view_cart"))
    return render_template("passenger/view_cart.html", reservations=reservations, role=util_functions.get_logged_in_user_role())


@app.route("/no_access")
def no_access():
    return render_template("no_access.html", role=util_functions.get_logged_in_user_role())


@app.route('/notready')
def not_ready_page():
    return render_template("not_built_yet.html", role=util_functions.get_logged_in_user_role())


if __name__ == "__main__":
    app.run(debug=True)
