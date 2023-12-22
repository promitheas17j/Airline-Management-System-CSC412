import sqlite3

db_file_name = 'database.db'
connection = sqlite3.connect(db_file_name)

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO passengers (fname, lname, passenger_email, password) VALUES (?, ?, ?, ?)",
            ("John", "Doe", "j.doe@test.com", "pass123")
)

cur.execute("INSERT INTO admins (fname, lname, admin_email, password, contact_no) VALUES (?, ?, ?, ?, ?)",
            ("Admin", "Admin", "admin@test.com", "secret", "+123 1234567890")
)

cur.execute("INSERT INTO flights (flight_no, international, depart_loc, arrive_loc, depart_date, depart_time, depart_country, arrive_country) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("AB1234", 1, "LCA", "SOF", "2023-12-25", "19:45:20", "Cyprus", "Bulgaria")
)

connection.commit()
connection.close()
