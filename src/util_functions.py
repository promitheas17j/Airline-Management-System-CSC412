from flask import session
import sqlite3

db_file_name = 'database.db'


def get_db_connection():
    conn = sqlite3.connect(db_file_name)
    conn.row_factory = sqlite3.Row

    return conn


def set_session_reservation_status(status):
    session["reserved"] = status


def get_session_reservation_status():
    return session.get("reserved")

def set_logged_in_role(role):
    session["logged_in_user_role"] = role
    print("logged_in_user_role: " + str(session.get("logged_in_user_role")))


def get_logged_in_user_role():
    return session.get("logged_in_user_role")


def set_logged_in_user_record(record):
    session["logged_in_user"] = record
    print("logged_in_user: " + str(session.get("logged_in_user")))


def get_logged_in_passenger_id():
    print("logged_in_passenger_id: " + str(session.get("logged_in_passenger_id")))
    return session.get("logged_in_user")[0]


def get_available_flights(passenger_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    query = """
        SELECT f.*, CASE WHEN r.passenger_id IS NOT NULL THEN 1 ELSE 0 END AS reserved_by_user
        FROM flights f
        LEFT JOIN reservations r ON f.flight_no = r.flight_no AND r.passenger_id = ?
    """

    cursor.execute(query, (passenger_id,))
    available_flights = cursor.fetchall()

    conn.close()

    for flight in available_flights:
        print(flight)

    return available_flights


def check_reservation_status(passenger_id, flight_number):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    existing_reservation = c.execute(
        "SELECT * FROM reservations WHERE passenger_id = ? AND flight_no = ?",
        (passenger_id, flight_number)
    ).fetchone()

    conn.close()

def update_flight(flight_no, depart_loc, arrive_loc, depart_date, depart_time, depart_country, arrive_country):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    query = """
        UPDATE flights
        SET depart_loc = ?, arrive_loc = ?, depart_date = ?, depart_time = ?, depart_country = ?, arrive_country = ?
        WHERE flight_no = ?
    """
    c.execute(query, (depart_loc, arrive_loc, depart_date, depart_time, depart_country, arrive_country, flight_no))
    
    conn.commit()
    conn.close()


def search_passenger(query):
    conn = get_db_connection()
    c = conn.cursor()

    results = None

    temp = c.execute("SELECT * FROM passengers WHERE passenger_email LIKE ?", (query,)).fetchall()
    
    if temp:
        results = (temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5])

    conn.close()

    print("RESULTS:")
    print(results)

    if not results:
        return None

    return results


def search_admin(query):
    conn = get_db_connection()
    c = conn.cursor()

    temp = c.execute("SELECT * FROM admins WHERE admin_email LIKE ?", (query,)).fetchall()
    results = (temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5])

    conn.close()

    return results


def search_flights(departure_airport, arrival_airport):
    conn = get_db_connection()
    c = conn.cursor()

    query = """
        SELECT flights.*,
               CASE WHEN reservations.passenger_id IS NOT NULL THEN 1 ELSE 0 END AS reserved_by_user
        FROM flights
        LEFT JOIN reservations ON flights.flight_no = reservations.flight_no
        WHERE depart_loc = ? AND arrive_loc = ?
    """
    c.execute(query, (departure_airport, arrival_airport,))
    matching_flights = c.fetchall()

    conn.close()
    return matching_flights
