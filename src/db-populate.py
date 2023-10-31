import sqlite3

db_locale = 'students.db'

con = sqlite3.connect(db_locale)
c = con.cursor()

c.execute("""
INSERT INTO contact_details (firstname, surname, street_address, suburb) VALUES
('David', 'Bowie', '11 Stardust Way', 'Wynnum'),
('Johny', 'Cash', '1 Dark Way', 'Blackall'),
('Joni', 'Mitchell', '2 Sides Lane', 'Canadia')
""")

con.commit()
con.close()
