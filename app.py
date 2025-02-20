import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import reservations

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_reservations = reservations.get_reservations()
    return render_template("index.html", reservations=all_reservations)

@app.route("/find_reservation")
def find_reservation():
    query = request.args.get("query")
    if query:
        results = reservations.find_reservations(query)
    else:
        query = ""
        results = []
    return render_template("find_reservation.html", query=query, results=results)

@app.route("/reservation/<int:reservation_id>")
def show_reservation(reservation_id):
    reservation = reservations.get_reservation(reservation_id)
    if not reservation:
        abort(404)
    return render_template("show_reservation.html", reservation=reservation)

@app.route("/new_reservation")
def new_reservation():
    require_login()
    return render_template("new_reservation.html")
@app.route("/create_reservation", methods=["POST"])
def create_reservation():
    require_login()
    name = request.form["name"]
    amount = request.form["amount"]
    time = request.form["time"]
    cat = request.form["cat"]
    user_id = session["user_id"]

    reservations.add_reservation(name, amount, time, cat, user_id)
    return redirect("/")
@app.route("/edit_reservation/<int:reservation_id>")
def edit_reservation(reservation_id):
    require_login()
    reservation = reservations.get_reservation(reservation_id)
    if not reservation:
        abort(404)
    if reservation["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_reservation.html", reservation=reservation)

@app.route("/update_reservation", methods=["POST"])
def update_reservation():
    require_login()
    reservation_id = request.form["reservation_id"]
    reservation = reservations.get_reservation(reservation_id)
    if not reservation:
        abort(404)
    if reservation["user_id"] != session["user_id"]:
        abort(403)
    name = request.form["name"]
    amount = request.form["amount"]
    time = request.form["time"]
    cat = request.form["cat"]
    reservations.update_reservation(reservation_id, name, amount, time, cat)
    return redirect("/reservation/" + str(reservation_id))

@app.route("/remove_reservation/<int:reservation_id>", methods=["GET", "POST"])
def remove_reservation(reservation_id):
    require_login()
    reservation = reservations.get_reservation(reservation_id)
    if not reservation:
        abort(404)
    if reservation["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_reservation.html", reservation=reservation)
    if request.method == "POST":
        if "remove" in request.form:
            reservations.remove_reservation(reservation_id)
            return redirect("/")
        else:
            return redirect("/reservation/" + str(reservation_id))

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":

            username = request.form["username"]
            password = request.form["password"]

            sql = "SELECT id, password_hash FROM users WHERE username = ?"
            result = db.query(sql, [username])[0]
            user_id = result["id"]
            password_hash = result["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"] = user_id
                session["username"] = username
                return redirect("/")
            else:
                return "VIRHE: väärä tunnus tai salasana"
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")