CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE varaukset (
    id INTEGER PRIMARY KEY,
    amount TEXT,
    time INTEGER,
    cat TEXT,
    user_id INTEGER REFERENCES users
);