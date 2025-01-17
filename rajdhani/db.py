"""
Module to interact with the database.
"""

from . import placeholders
from . import db_ops

from . import config

from sqlalchemy import MetaData, create_engine, select, insert, text
from sqlalchemy import Table, Column, Integer, Float, String
from sqlalchemy import and_, or_

db_ops.ensure_db()

engine = create_engine(config.db_uri)
metadata_obj = MetaData(bind=engine)
train_table = Table(
    "train",
    metadata_obj,
    autoload=True,
)
booking_table = Table(
    "booking",
    metadata_obj,
    autoload=True,
)

def search_stations(q):
    """Returns the top ten stations matching the given query string.

    This is used to get show the auto complete on the home page.

    The q is the few characters of the station name or
    code entered by the user.
    """
    query = text(
        "SELECT code, name FROM station WHERE code = :q OR UPPER(name) LIKE :like",
    )
    with engine.connect() as conn:
        result = conn.execute(
            query,
            {"q": q.upper(), "like": f"%{q.upper()}%"}
        )
        return [{"code": row.code, "name": row.name} for row in result]


def search_trains(
        from_station_code,
        to_station_code,
        ticket_class=None,
        departure_date=None,
        departure_time=[],
        arrival_time=[]):
    """Returns all the trains that source to destination stations on
    the given date. When ticket_class is provided, this should return
    only the trains that have that ticket class.

    This is used to get show the trains on the search results page.
    """
    # TODO: This task should mention how input is taken for ticket
    # class.
    stmt = select(train_table).where(
        train_table.c.from_station_code == from_station_code,
        train_table.c.to_station_code == to_station_code,
    )
    if ticket_class is not None:
        stmt = stmt.where(
            get_ticket_class_column(ticket_class) == 1,
        )
    if departure_time:
        conditions = [
            get_slot_condition(slot, column=train_table.c.departure)
            for slot in departure_time
        ]
        stmt = stmt.where(
            conditions[0] if len(conditions) == 1 else
            or_(*conditions)
        )
    if arrival_time:
        conditions = [
            get_slot_condition(slot, column=train_table.c.arrival)
            for slot in arrival_time
        ]
        stmt = stmt.where(
            conditions[0] if len(conditions) == 1 else
            or_(*conditions)
        )

    stmt = stmt.where(
        train_table.c.departure
    )

    with engine.connect() as conn:
        result = conn.execute(stmt)
        return [make_train(row) for row in result]


def make_train(row):
    return {
        "number": row.number,
        "name": row.name,
        "from_station_code": row.from_station_code,
        "from_station_name": row.from_station_name,
        "to_station_code": row.to_station_code,
        "to_station_name": row.to_station_name,
        "departure": row.departure,
        "arrival": row.arrival,
        "duration_h": row.duration_h,
        "duration_m": row.duration_m,
    }

def get_ticket_class_column(ticket_class):
    return {
        "SL": train_table.c.sleeper,
        "3A": train_table.c.third_ac,
        "2A": train_table.c.second_ac,
        "1A": train_table.c.first_ac,
        "CC": train_table.c.chair_car,
    }[ticket_class]

def get_slot_condition(slot, column):
    if slot == "slot1": return and_(column >= "00:00", column < "08:00")
    if slot == "slot2": return and_(column >= "08:00", column < "12:00")
    if slot == "slot3": return and_(column >= "12:00", column < "16:00")
    if slot == "slot4": return and_(column >= "16:00", column < "20:00")
    if slot == "slot5": return and_(column >= "20:00", column < "24:00")
    raise Exception("unknown slot")

def get_schedule(train_number):
    """Returns the schedule of a train.
    """
    stmt = text("SELECT * FROM schedule WHERE train_number = :train_number")
    with engine.connect() as conn:
        result = conn.execute(stmt, train_number=train_number)
        return [
            {
                "station_code": row.station_code,
                "station_name": row.station_name,
                "day": row.day,
                "arrival": row.arrival,
                "departure": row.departure,
            } for row in result
        ]

def book_ticket(train_number, ticket_class, departure_date, passenger_name, passenger_email):
    """Book a ticket for passenger
    """
    (
        "INSERT INTO booking "
        "(train_number, from_station_code, to_station_code, "
        "passenger_name, passenger_email, ticket_class, date)"
        "VALUES "
        "(:train_number, :from_station_code, :to_station_code,"
        " :passenger_name, :passenger_email, :ticket_class, :departure_date)"
    )
    with engine.connect() as conn:
        train = get_train_by_number(conn, train_number)
        stmt = insert(booking_table).values(
            train_number=train_number,
            from_station_code=train.from_station_code,
            to_station_code=train.to_station_code,
            passenger_name=passenger_name,
            passenger_email=passenger_email,
            ticket_class=ticket_class,
            date=departure_date)
        result = conn.execute(stmt)
        id = result.inserted_primary_key[0]
        return make_booking(get_booking_by_id(conn, id))

    return placeholders.TRIPS[0]

def get_booking_by_id(conn, id):
    stmt = text("select * from booking where id=:id")
    return next(conn.execute(stmt, {"id": id}))

def get_train_by_number(conn, train_number):
    stmt = select(train_table).where(train_table.c.number == train_number)
    return next(conn.execute(stmt))

def make_booking(row):
    with engine.connect() as conn:
        train = get_train_by_number(conn, row.train_number)
    return {
        "train_number": row.train_number,
        "train_name": train.name,
        "from_station_code": row.from_station_code,
        "from_station_name": train.from_station_name,
        "to_station_code": row.to_station_code,
        "to_station_name": train.to_station_name,
        "ticket_class": row.ticket_class,
        "date": row.date,
        "passenger_name": row.passenger_name,
        "passenger_email": row.passenger_email,
    }

def get_trips(email):
    """Returns the bookings made by the user
    """
    stmt = select(booking_table).where(
        booking_table.c.passenger_email == email
    )
    with engine.connect() as conn:
        result = conn.execute(stmt)
        return [make_booking(row) for row in result]
