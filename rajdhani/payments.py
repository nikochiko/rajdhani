import stripe
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Text, Integer, ForeignKey
from sqlalchemy.sql import select, and_

from . import db
from .db import pythonify


stripe.api_key = "sk_test_rDLIewViMw0MtdrF8UH3jHao00OFfTN155"

tickets = Table("tickets", db.metadata_obj,
                Column("id", Integer, primary_key=True),
                Column("train_number", Text, ForeignKey("train.number")),
                Column("ticket_class", Text),
                Column("price", Integer),
                Column("stripe_product_id", Text),
                Column("stripe_price_id", Text))


def create_checkout_session(train_number, ticket_class, success_url, cancel_url):
    price_id = get_or_create_price_id(train_number, ticket_class)

    return stripe.checkout.Session.create(
        line_items=[
            {
                "price": price_id,
                "quantity": 1
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
    )


def get_or_create_price_id(train_number, ticket_class):
    """Create 'Product' and 'Price' objects in Stripe
    """
    create_tickets_table_if_needed()

    with db.engine.connect() as conn:
        result = conn.execute(
            select(tickets)
            .where(
                and_(tickets.c.train_number == train_number,
                     tickets.c.ticket_class == ticket_class)
            )
        )
        result = pythonify(result)
        if result:
            ticket = result[0]
            return ticket["stripe_price_id"]

        price_rs = get_ticket_price(train_number, ticket_class)  # rupees
        product = stripe.Product.create(
            name=f"Train {train_number}: {ticket_class}",
            default_price_data={
                "currency": "INR",
                "unit_amount": price_rs * 100 # paise
            }
        )
        with conn.begin():
            conn.execute(
                tickets.insert(), {
                    "train_number": train_number,
                    "ticket_class": ticket_class,
                    "price": price_rs,
                    "stripe_product_id": product["id"],
                    "stripe_price_id": product["default_price"]
                }
            )

        return product["default_price"]


def create_tickets_table_if_needed():
    tickets.create(db.engine, checkfirst=True)


def get_ticket_price(train_number, ticket_class):
    """Return ticket price in rupees

    Doesn't take into account from/to station for now.
    """
    if ticket_class == "sleeper":
        return 600
    elif ticket_class == "third_ac":
        return 1000
    elif ticket_class == "second_ac":
        return 1400
    elif ticket_class == "first_ac":
        return 1800
    elif ticket_class == "first_class":
        return 2200
    elif ticket_class == "chair_car":
        return 800
