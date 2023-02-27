"""Email notifications on bookings.
"""
from . import config

from textwrap import dedent
from smtplib import SMTP

# client = SMTP(host=config.smtp_hostname, port=int(config.smtp_port))
# if config.smtp_username and config.smtp_password:
#     client.login(config.smtp_username, config.smtp_password)


def send_booking_confirmation_email(booking):
    """Sends a confirmation email on successful booking.

    The argument `booking` is a row in the database that contains the following fields:

        id, name, email, train_number, train_name, ticket_class, date
    """
    name, email, train_name, train_number, date, ticket_class = (
        booking["passenger_name"], booking["passenger_email"],
        booking["train_name"], booking["train_number"],
        booking["date"], booking["ticket_class"]
    )

    text = dedent(f"""\
    Subject: Booking confirmation for your train

    Hey {name},

    Your booking on train {train_name} ({train_number})
    is successful. You are schedeuled to leave on {date}, and
    your ticket is in class {ticket_class}.

    Best,
    Rajdhani Ticket Service
    """)
    client.sendmail("nikochiko@rajdhani.pipal.in", [email], text)
