DROP TABLE IF EXISTS passengers;

CREATE TABLE passengers (
	passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
	fname VARCHAR(254) NOT NULL,
	lname VARCHAR(254) NOT NULL,
	passenger_email VARCHAR(254) NOT NULL,
	password VARCHAR(254) NOT NULL,
	passport_no INTEGER,

	UNIQUE (passenger_email)
);

DROP TABLE IF EXISTS admins;

CREATE TABLE admins (
	admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
	fname VARCHAR(254) NOT NULL,
	lname VARCHAR(254) NOT NULL,
	admin_email VARCHAR(254) NOT NULL,
	password VARCHAR(254) NOT NULL,
	contact_no VARCHAR(254) NOT NULL,

	UNIQUE (admin_email)
);

DROP TABLE IF EXISTS flights;

CREATE TABLE flights (
	flight_no VARCHAR(6),
	international BOOLEAN,
	depart_loc CHAR(3),
	arrive_loc CHAR(3),
	depart_date DATE,
	depart_time TIME,
	depart_country VARCHAR(254),
	arrive_country VARCHAR(254),
	
	UNIQUE(flight_no)
);

DROP TABLE IF EXISTS reservations;

CREATE TABLE reservations (
	reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
	passenger_id INTEGER,
	flight_no VARCHAR(6),

	FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
	FOREIGN KEY (flight_no) REFERENCES flights(flight_no)
);
