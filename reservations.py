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

def update_reservation(reservation_id, name, amount, time, cat):
    sql = """UPDATE reservations SET name = ?,
                                     amount = ?,
                                     time = ?,
                                     cat = ?
                                WHERE id = ?"""
    db.execute(sql, [name, amount, time, cat, reservation_id])

def remove_reservation(reservation_id):
    sql = "DELETE FROM reservations WHERE id = ?"
    db.execute(sql, [reservation_id])

def find_reservations(query):
    sql = """SELECT id, name
                FROM reservations
                WHERE name LIKE ? OR cat LIKE ?
                ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])