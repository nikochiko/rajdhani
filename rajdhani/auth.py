import secrets
import smtplib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask import current_app, request, session
import jwt

from . import config


@dataclass
class User:
    email: str


def create_magic_link(email):
    # NOTE: this encodes email plainly in a JWT, this can
    # be read by anyone who has access to this token.
    expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=600)
    token = jwt.encode({"exp": expiration, "email": email},
                       current_app.secret_key,
                       algorithm="HS256")

    return f"{request.url_root}magic-link/login/{token}"


def decode_magic_token(token):
    try:
        decoded = jwt.decode(token, current_app.secret_key,
                             algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return None
    else:
        return decoded["email"]


def send_magic_link(email):
    hostname, port = config.smtp["hostname"], config.smtp["port"]
    username, password = config.smtp.get("username"), config.smtp.get("password")

    with smtplib.SMTP(hostname, port) as smtp:
        smtp.ehlo("kaustubh.rajdhani.pipal.in")
        if username and password:
            smtp.starttls()
            smtp.login(username, password)

        magic_link = create_magic_link(email)
        content = f"Hello, {email}!\n\nThis is your magic link: {magic_link}"
        smtp.sendmail("Kaustubh <kaustubh@rajdhani.pipal.in>",
                      [email], content)


def get_secret_key():
    ensure_secret_key_file()
    return open(config.secret_key_file).read()


def ensure_secret_key_file():
    if not Path(config.secret_key_file).is_file():
        with open(config.secret_key_file, "w") as f:
            f.write(secrets.token_hex())


def login_user(email):
    session["user_email"] = email


def get_logged_in_user_email():
    return session.get("user_email")
