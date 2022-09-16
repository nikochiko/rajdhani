import sqlite3

from flask import Flask, jsonify, redirect, render_template, request
from urllib.parse import urlparse
from . import config
from . import db
from . import db_ops
from . import payments


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", config=config)

@app.route("/api/stations")
def api_stations():
    q = request.args.get("q")
    stations = db.search_stations(q)
    return jsonify(stations)

@app.route("/api/search")
def api_search():
    from_station = request.args.get("from")
    to_station = request.args.get("to")
    ticket_class = request.args.get("class")
    date = request.args.get("date")

    trains = db.search_trains(from_station, to_station, ticket_class, date)
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

@app.route("/checkout")
def checkout():
    train_number = request.args.get("train_number")
    ticket_class = request.args.get("ticket_class")

    if not train_number or not ticket_class:
        return "train_number or ticket_class is not given", 400

    success_url = request.url_root + "payment/success"
    cancel_url = request.url_root + "payment/cancel"

    try:
        checkout_session = payments.create_checkout_session(
            train_number, ticket_class,
            success_url=success_url, cancel_url=cancel_url
        )
    except Exception as e:
        return str(e), 500

    return redirect(checkout_session.url, code=303)


@app.route("/payment/success")
def payment_success():
    return "Thanks! Your order was successful"


@app.route("/payment/cancel")
def payment_cancel():
    return "Oops. Your order was cancelled."
