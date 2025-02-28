import db

def get_all_classes():
    sql = "SELECT name, value FROM classes ORDER BY id"
    result = db.query(sql)
    classes = {}
    for name, value in result:
        classes[name] = []
    for name, value in result:
        classes[name].append(value)

    return classes

def add_reservation(name, amount, time, cat, user_id, classes):
    sql = """INSERT INTO reservations (name, amount, time, cat, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [name, amount, time, cat, user_id])

    reservation_id = db.last_insert_id()
    sql = "INSERT INTO reservation_classes (reservation_id, name, value) VALUES (?, ?, ?)"
    for name, value in classes:
        db.execute(sql, [reservation_id, name, value])

def add_comment(reservation_id, user_id, comment):
    sql = """INSERT INTO comments (reservation_id, user_id, comment)
            VALUES (?, ?, ?)"""
    db.execute(sql, [reservation_id, user_id, comment])

def get_comments(reservation_id):
    sql = """SELECT comments.comment, users.id user_id, users.username
                FROM comments, users
                WHERE comments.reservation_id = ? AND comments.user_id = users.id
                ORDER BY comments.id DESC"""
    return db.query(sql, [reservation_id])

def get_classes(reservation_id):
    sql = "SELECT name, value FROM reservation_classes WHERE reservation_id = ?"
    return db.query(sql, [reservation_id])

def get_reservations():
    sql = "SELECT id, name FROM reservations ORDER BY id DESC"
    return db.query(sql)

def get_reservation(reservation_id):
    sql = """SELECT reservations.id,
                    reservations.name,
                    reservations.amount,
                    reservations.time,
                    users.id user_id,
                    reservations.cat,
                    users.username
             FROM reservations, users
             WHERE reservations.user_id = users.id AND
                   reservations.id = ?"""
    result = db.query(sql, [reservation_id])
    return result[0] if result else None

def update_reservation(reservation_id, name, amount, time, cat, classes):
    sql = """UPDATE reservations SET name = ?,
                                     amount = ?,
                                     time = ?,
                                     cat = ?
                                WHERE id = ?"""
    db.execute(sql, [name, amount, time, cat, reservation_id])

    sql = "DELETE FROM reservation_classes WHERE reservation_id = ?"
    db.execute(sql, [reservation_id])

    sql = "INSERT INTO reservation_classes (reservation_id, name, value) VALUES (?, ?, ?)"
    for name, value in classes:
        db.execute(sql, [reservation_id, name, value])

def remove_reservation(reservation_id):
    sql = "DELETE FROM reservation_classes WHERE reservation_id = ?"
    db.execute(sql, [reservation_id])
    sql = "DELETE FROM reservations WHERE id = ?"
    db.execute(sql, [reservation_id])

def find_reservations(query):
    sql = """SELECT id, name
                FROM reservations
                WHERE name LIKE ? OR cat LIKE ?
                ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])