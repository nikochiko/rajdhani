import requests
import sqlite3
from pathlib import Path

from .config import db_path, db_init_url


def init_db():
    download_file(db_init_url, db_path)


def reset_db():
    Path(db_path).unlink(missing_ok=True)
    init_db()


def ensure_db():
    if not Path(db_path).is_file():
        init_db()


def download_file(url, location):
    response = requests.get(url)
    with open(location, "wb") as f:
        f.write(response.content)


def get_conn():
    return sqlite3.connect(db_path)


def exec_query(q, commit=False):
    conn = get_conn()
    curs = conn.cursor()

    try:
        curs.execute(q)
        if commit:
            conn.commit()

        columns = [c[0] for c in curs.description]
        rows = curs.fetchall()
    finally:
        conn.close()

    return columns, rows
