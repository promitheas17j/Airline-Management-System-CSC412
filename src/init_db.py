import sqlite3

db_file_name = 'database.db'
connection = sqlite3.connect(db_file_name)

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute("INSERT INTO admins (fname, lname, admin_email, password, contact_no) VALUES (?, ?, ?, ?, ?)",
            ("Admin", "Admin", "admin@test.com", "secret", "+123 1234567890")
)

connection.commit()
connection.close()
