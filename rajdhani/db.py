"""
Module to interact with the database.
"""

from math import sin, cos, sqrt, atan2
from sqlalchemy import MetaData, Table, create_engine, func, or_, and_
from sqlalchemy.sql import select

from . import placeholders
from . import db_ops
from . import config

db_ops.ensure_db()

engine = create_engine(config.db_uri)
metadata_obj = MetaData()
train = Table("train", metadata_obj, autoload_with=engine)
station = Table("station", metadata_obj, autoload_with=engine)


def pythonify(sqla_result):
    return [dict(row) for row in sqla_result]


def search_stations(q):
    """Returns the top ten stations matching the given query string.

    This is used to get show the auto complete on the home page.

    The q is the few characters of the station name or
    code entered by the user.
    """

    with engine.connect() as conn:
        result = conn.execute(
            select(station)
            .where(
                or_(func.upper(station.c.name).like(f"%{q.upper()}%"),
                    func.upper(station.c.code) == q.upper())
            )
            .limit(10)
        )

        return pythonify(result)

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
    alt_froms = get_alternative_stations(from_station_code)
    alt_tos = get_alternative_stations(to_station_code)

    with engine.connect() as conn:
        result = conn.execute(
            select(
                train.c.number,
                train.c.name,
                train.c.from_station_code,
                train.c.from_station_name,
                train.c.to_station_code,
                train.c.to_station_name,
                train.c.departure,
                train.c.arrival,
                train.c.duration_h,
                train.c.duration_m,
            )
            .where(
                and_(train.c.from_station_code.in_(alt_froms),
                     train.c.to_station_code.in_(alt_tos),
                     ticket_class and getattr(train.c, ticket_class) == 1 or True)
            )
        )

        return pythonify(result)

def get_schedule(train_number):
    """Returns the schedule of a train.
    """
    return placeholders.SCHEDULE

def book_ticket(train_number, ticket_class, departure_date, passenger_name, passenger_email):
    """Book a ticket for passenger
    """
    # TODO: make a db query and insert a new booking
    # into the booking table

    return placeholders.TRIPS[0]

def get_trips(email):
    """Returns the bookings made by the user
    """
    # TODO: make a db query and get the bookings
    # made by user with `email`

    return placeholders.TRIPS


def get_alternative_stations(station_code):
    with engine.connect() as conn:
        result = conn.execute(
            select(station.c.code, station.c.latitude, station.c.longitude)
            .where(station.c.code == station_code)
        )
        og_station = dict(next(result))

        lat_bounds = (og_station["latitude"]-0.5, og_station["latitude"]+0.5)
        long_bounds = (og_station["longitude"]-0.5, og_station["longitude"]+0.5)

        result = conn.execute(
            select(station.c.code, station.c.latitude, station.c.longitude)
            .where(
                and_(station.c.latitude.between(*lat_bounds),
                     station.c.longitude.between(*long_bounds))
            )
        )
        sane_result = pythonify(result)

    acceptable_distance = 600  # imaginary units?

    def distance(stn):
        dist = get_distance_by_latlon(
            og_station["latitude"], og_station["longitude"],
            stn["latitude"], stn["longitude"]
        )
        return dist
    return [stn["code"]
            for stn in sane_result if distance(stn) < acceptable_distance]


def get_distance_by_latlon(lat1, lon1, lat2, lon2):
    """
    Haversine formula to get distance from lat and long.
    """

    R = 6373.0  # radius of earth, in km

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance
