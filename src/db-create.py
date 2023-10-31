import sqlite3

db_locale = 'students.db'

con = sqlite3.connect(db_locale)
c = con.cursor()

c.execute("""
CREATE TABLE contact_details
(id INTEGER PRIMARY KEY AUTOINCREMENT,
firstname TEXT,
surname TEXT,
street_address TEXT,
suburb TEXT
)
""")

con.commit()
con.close()
