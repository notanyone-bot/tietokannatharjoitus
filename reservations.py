import db
def add_reservation(amount, time, cat, user_id):
    sql = """INSERT INTO varaukset (amount, time, cat, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [amount, time, cat, user_id])