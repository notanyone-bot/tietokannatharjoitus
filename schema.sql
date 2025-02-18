CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    amount TEXT,
    time INTEGER,
    cat TEXT,
    user_id INTEGER REFERENCES users
);