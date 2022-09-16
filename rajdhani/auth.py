import secrets
import smtplib
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from flask import request, session, g

from . import config


@dataclass
class User:
    id: int
    name: str
    email: str

    def _create_magic_link(self):
        magic_code = secrets.token_urlsafe(16)
        with sqlite3.connect(config.db_path) as conn:
            conn.execute(
                "insert into magic_link_code (code, user_id) values (?, ?)",
                (magic_code, self.id)
            )

        return f"{request.url_root}magic-link/login/{magic_code}"

    def send_magic_link(self):
        # TODO: use `config.smtp` to send an email
        hostname, port = config.smtp["hostname"], config.smtp["port"]
        username, password = config.smtp.get("username"), config.smtp.get("password")

        with smtplib.SMTP(hostname, port) as smtp:
            smtp.ehlo("kaustubh.rajdhani.pipal.in")
            if username and password:
                smtp.starttls()
                smtp.login(username, password)

            magic_link = self._create_magic_link()
            content = f"Hello, {self.name}!\n\nThis is your magic link: {magic_link}"
            smtp.sendmail("Kaustubh <kaustubh@rajdhani.pipal.in>",
                          [self.email], content)


def authenticate():
    if "token" in session:
        g.user = get_user_by_token(session["token"])


def get_secret_key():
    ensure_secret_key_file()
    return open(config.secret_key_file).read()


def ensure_secret_key_file():
    if not Path(config.secret_key_file).is_file():
        with open(config.secret_key_file, "w") as f:
            f.write(secrets.token_hex())


def get_user_by_token(token):
    with sqlite3.connect(config.db_path) as conn:
        curs = conn.cursor()
        curs.execute("select id, name, email from user where token = ?", (token,))
        row = curs.fetchone()

    return row and User(*row) or None


def get_user_by_email(email):
    with sqlite3.connect(config.db_path) as conn:
        curs = conn.cursor()
        curs.execute("select id, name, email from user where email = ?", (email,))
        row = curs.fetchone()

    return row and User(*row) or None


def create_user(name, email):
    # TODO: validate email?
    with sqlite3.connect(config.db_path) as conn:
        curs = conn.execute("insert into user (name, email) values (?, ?) returning id", (name, email))
        user_id = (row := curs.fetchone()) and row[0]

    return user_id


def login_user(user_id):
    token = secrets.token_hex()
    with sqlite3.connect(config.db_path) as conn:
        conn.execute("update user set token = ? where id = ?", (token, user_id))

    session["token"] = token


def invalidate_magic_link_code(code):
    with sqlite3.connect(config.db_path) as conn:
        conn.execute("delete from magic_link_code where code = ?", (code,))
