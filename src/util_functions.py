from flask import session
import sqlite3


def get_logged_in_passenger_id():
    return session.get("logged_in_user")[0]


def get_logged_in_user_role():
    return session.get("logged_in_user_role")


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
