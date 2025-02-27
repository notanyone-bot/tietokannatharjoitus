import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import config
import reservations
import re
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_reservations = reservations.get_reservations()
    return render_template("index.html", reservations=all_reservations)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    reservations = users.get_reservations(user_id)
    return render_template("show_user.html", user=user, reservations=reservations)

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
    classes = reservations.get_classes(reservation_id)
    return render_template("show_reservation.html", reservation=reservation, classes=classes)

@app.route("/new_reservation")
def new_reservation():
    require_login()
    classes = reservations.get_all_classes()
    return render_template("new_reservation.html", classes=classes)
@app.route("/create_reservation", methods=["POST"])
def create_reservation():
    require_login()
    name = request.form["name"]
    if not name or len(name) > 30:
        abort(403)
    amount = request.form["amount"]
    if not amount or not re.search("^[0-9][0-9]{0,3}$", amount):
        abort(403)
    time = request.form["time"]
    if not time or len(time) > 10:
        abort(403)
    cat = request.form["cat"]
    if len(cat) > 20:
        abort(403)
    user_id = session["user_id"]
    all_classes = reservations.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_name, class_value = entry.split(":")
            if class_name not in all_classes:
                abort(403)
            if class_value not in all_classes[class_name]:
                abort(403)
            classes.append((class_name, class_value))

    reservations.add_reservation(name, amount, time, cat, user_id, classes)
    return redirect("/")
@app.route("/edit_reservation/<int:reservation_id>")
def edit_reservation(reservation_id):
    require_login()
    reservation = reservations.get_reservation(reservation_id)
    if not reservation:
        abort(404)
    if reservation["user_id"] != session["user_id"]:
        abort(403)
    all_classes = reservations.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in reservations.get_classes(reservation_id):
        classes[entry["name"]] = entry["value"]

    return render_template("edit_reservation.html", reservation=reservation, classes=classes, all_classes=all_classes)

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
    if not name or len(name) > 30:
        abort(403)
    amount = request.form["amount"]
    if not amount or not re.search("^[0-9][0-9]{0,3}$", amount):
        abort(403)
    time = request.form["time"]
    if not time or len(time) > 10:
        abort(403)
    cat = request.form["cat"]
    if len(cat) > 20:
        abort(403)
    all_classes = reservations.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_name, class_value = entry.split(":")
            if class_name[0] not in all_classes:
                abort(403)
            if class_value not in all_classes[class_name]:
                abort(403)
            classes.append((class_name, class_value))

    reservations.update_reservation(reservation_id, name, amount, time, cat, classes)
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
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return "Tunnus luotu"
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

            user_id = users.check_login(username, password)
            if user_id:
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