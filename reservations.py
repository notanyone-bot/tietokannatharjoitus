import db
def add_reservation(name, amount, time, cat, user_id):
    sql = """INSERT INTO reservations (name, amount, time, cat, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [name, amount, time, cat, user_id])

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
    return db.query(sql, [reservation_id])[0]
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