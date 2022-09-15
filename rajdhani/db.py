"""
Module to interact with the database.
"""

from sqlalchemy import MetaData, Table, create_engine, func, or_
from sqlalchemy.sql import select

from . import db_ops
from . import config

db_ops.ensure_db()

engine = create_engine(config.db_uri)
metadata_obj = MetaData()
train = Table("train", metadata_obj, autoload_with=engine)
station = Table("station", metadata_obj, autoload_with=engine)


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

        return [dict(row) for row in result]


def search_trains(from_station, to_station, date, ticket_class):
    """Returns all the trains that source to destination stations on
    the given date. When ticket_class is provided, this should return
    only the trains that have that ticket class.

    This is used to get show the trains on the search results page.
    """
    # TODO: make a db query to get the matching trains
    # and replace the following dummy implementation

    return [
        {
            "train_number": "12028",
            "train_name": "Shatabdi Exp",
            "from_station_code": "SBC",
            "from_station_name": "Bangalore",
            "to_station_code": "MAS",
            "to_station_name": "Chennai",
            "start_date": date,
            "start_time": "06:00",
            "end_date":  date,
            "end_time": "11:00",
            "duration": "05:00"
        },
        {
            "train_number": "12608",
            "train_name": "Lalbagh Exp",
            "from_station_code": "SBC",
            "from_station_name": "Bangalore",
            "to_station_code": "MAS",
            "to_station_name": "Chennai",
            "start_date": date,
            "start_time": "06:20",
            "end_date":  date,
            "end_time": "12:15",
            "duration": "05:55"
        },
    ]
