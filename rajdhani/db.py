"""
Module to interact with the database.
"""

from sqlalchemy import MetaData, Table, create_engine, func, or_, and_
from sqlalchemy.sql import select

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
                or_(func.upper(station.c.name).startswith(q),
                    func.upper(station.c.code).startswith(q))
            )
            .limit(10)
        )

        return pythonify(result)


def search_trains(from_station, to_station, date, ticket_class):
    """Returns all the trains that source to destination stations on
    the given date. When ticket_class is provided, this should return
    only the trains that have that ticket class.

    This is used to get show the trains on the search results page.
    """

    with engine.connect() as conn:
        result = conn.execute(
            select(
                train.c.number.label("train_number"),
                train.c.name.label("train_name"),
                train.c.from_station_code,
                train.c.from_station_name,
                train.c.to_station_code,
                train.c.to_station_name,
                train.c.departure.label("start_time"),
                train.c.arrival.label("end_time"),
                train.c.duration_h,
                train.c.duration_m,
            )
            .where(
                and_(train.c.from_station_code == from_station,
                     train.c.to_station_code == to_station)
            )
        )

        sane_result = pythonify(result)

    for trn in sane_result:
        duration_h, duration_m = trn.pop("duration_h"), trn.pop("duration_m")
        trn.update(duration=f"{duration_h}:{duration_m}")
        trn.update(start_date="Today", end_date="Today")
        trn["start_time"] = trn["start_time"].rsplit(":", maxsplit=1)[0]
        trn["end_time"] = trn["end_time"].rsplit(":", maxsplit=1)[0]

    return sane_result
