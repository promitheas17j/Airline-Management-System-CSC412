DROP TABLE IF EXISTS users;

CREATE TABLE users (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT,
	fname VARCHAR(254) NOT NULL,
	lname VARCHAR(254) NOT NULL,
	email VARCHAR(254) NOT NULL,
	password VARCHAR(254) NOT NULL,

	UNIQUE (email)
);

DROP TABLE IF EXISTS flights;

CREATE TABLE flights (
	flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
	depart_loc CHAR(3),
	arrive_loc CHAR(3),
	depart_date DATETIME,
	arrive_date DATETIME,
	adult_ticket BOOLEAN,
	round_trip BOOLEAN
);
