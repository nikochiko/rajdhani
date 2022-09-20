import sqlite3
from datetime import datetime

from flask import Flask, abort, jsonify, redirect, render_template, request
from urllib.parse import urlparse
from . import config
from . import db
from . import db_ops
from . import auth
from . import notifications

app = Flask(__name__)

app.secret_key = config.secret_key


@app.context_processor
def add_context():
    return dict(config=config)

@app.route("/")
def index():
    from_station_code = request.args.get("from_station_code")
    to_station_code = request.args.get("to_station_code")
    ticket_class = request.args.get("class")
    departure_date = request.args.get("date")
    departure_time = request.args.getlist("dt")
    arrival_time = request.args.getlist("at")

    if from_station_code and to_station_code:
        print("search-trains")
        trains = db.search_trains(
            from_station_code=from_station_code,
            to_station_code=to_station_code,
            ticket_class=ticket_class,
            departure_date=departure_date,
            departure_time=departure_time,
            arrival_time=arrival_time)
    else:
        trains = None

    today = datetime.today().strftime("%Y-%m-%d")
    return render_template("index.html", trains=trains, args=request.args, today=today)

@app.route("/trains/<number>")
def schedule(number):
    schedule = db.get_schedule(number)
    return render_template("schedule.html", schedule=schedule, train_number=number)

@app.route("/api/flags")
def api_flags():
    flags = {k: v for k, v in config.__dict__.items() if k.startswith("flag_")}
    return jsonify(flags)

@app.route("/api/stations")
def api_stations():
    q = request.args.get("q")
    stations = db.search_stations(q)
    return jsonify(stations)

@app.route("/api/search")
def api_search():
    from_station_code = request.args.get("from")
    to_station_code = request.args.get("to")
    ticket_class = request.args.get("class")
    departure_time = request.args.getlist("dt")
    arrival_time = request.args.getlist("at")

    trains = db.search_trains(
        from_station_code=from_station_code,
        to_station_code=to_station_code,
        ticket_class=ticket_class,
        departure_time=departure_time,
        arrival_time=arrival_time)

    trains = [dict(t) for t in trains]
    return jsonify(trains)

@app.route("/search")
def search():
    from_station = request.args.get("from")
    to_station = request.args.get("to")
    ticket_class = request.args.get("class")
    date = request.args.get("date")

    trains = db.search_trains(from_station, to_station, ticket_class, date)
    return render_template("search.html",
        trains=trains,
        from_station=from_station,
        to_station=to_station,
        ticket_class=ticket_class,
        date=date)

@app.route("/db/reset")
def reset_db():
    db_ops.reset_db()
    return "ok"

@app.route("/db/exec")
def exec_db():
    q = request.args.get("q")
    columns, rows = db_ops.exec_query(q)
    return {
        "columns": columns,
        "rows": rows
    }

@app.route("/data-explorer")
def explore_data():
    q = request.args.get("q")

    error, columns, rows = None, None, None
    if q:
        try:
            columns, rows = db_ops.exec_query(q)
        except (sqlite3.Error, sqlite3.Warning) as e:
            error = str(e)

    return render_template(
        "data_explorer.html",
        error=error, columns=columns, rows=rows, query=q,
    )

@app.route("/progress")
def progress():
    url = urlparse(request.base_url)
    username = url.hostname.split(".", maxsplit=1)[0]
    redirect_url = f"{config.base_status_page_url}/{username}"

    return redirect(redirect_url, code=302)

@app.route("/book-ticket", methods=["GET", "POST"])
def book_ticket_page():
    if request.method == "POST":
        booking = db.book_ticket(train_number=request.form.get("train"),
                       ticket_class=request.form.get("class"),
                       departure_date=request.form.get("date"),
                       passenger_name=request.form.get("passenger_name"),
                       passenger_email=request.form.get("passenger_email"))
        notifications.send_booking_confirmation_email(booking)

        return redirect("/thank-you")
    else:
        email = auth.get_logged_in_user_email()

        train_number = request.args.get("train")
        ticket_class = request.args.get("class")
        date = request.args.get("date")

    return render_template("book_ticket.html",
                           train_number=train_number,
                           ticket_class=ticket_class,
                           date=date, email=email)

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/bookings")
def my_bookings():
    email = auth.get_logged_in_user_email()
    if not email:
        return redirect("/login")

    bookings = db.get_trips(email)
    return render_template("bookings.html", bookings=bookings)

@app.route("/hello")
def hello():
    """Simple endpoint to check the authenticated user is
    """
    return render_template("hello.html", user=auth.get_logged_in_user_email())

@app.route("/login")
def login():
    if email := request.args.get("email"):
        auth.login(email)
        return redirect("/hello")

    return render_template("login.html")

@app.route("/logout")
def logout():
    auth.logout()
    return redirect("/")
