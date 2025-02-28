CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    amount INTEGER,
    time TEXT,
    cat TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    value TEXT
);


CREATE TABLE reservation_classes (
    id INTEGER PRIMARY KEY,
    reservation_id INTEGER REFERENCES reservations,
    name TEXT,
    value TEXT
);