import sqlite3

db_file_name = 'database.db'
connection = sqlite3.connect(db_file_name)

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (fname, lname, email, password) VALUES (?, ?, ?, ?)",
            ("John", "Doe", "j.doe@test.com", "pass123")
)

cur.execute("INSERT INTO users (fname, lname, email, password) VALUES (?, ?, ?, ?)",
            ("Jane", "Smith", "j.smith@test.com", "secret")
)

cur.execute("INSERT INTO flights (depart_loc, arrive_loc, depart_date, arrive_date, adult_ticket, round_trip) VALUES (?, ?, ?, ?, ?, ?)",
            ("LCA", "SOF", "2023-12-25 13:30:45", "2023-12-25 15:45:00", 1, 0)
)

connection.commit()
connection.close()
