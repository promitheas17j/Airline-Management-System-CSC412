import sqlite3

db_locale = 'students.db'

con = sqlite3.connect(db_locale)
c = con.cursor()

c.execute("""
SELECT * FROM contact_details
""")

student_info = c.fetchall()

for student in student_info:
    print(student_info)

con.commit()
con.close()
