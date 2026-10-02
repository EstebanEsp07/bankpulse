from datetime import datetime, timezone

from ..extensions import db


class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    cuisine = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    seats_per_day = db.Column(db.Integer, nullable=False)
    deposit_cents = db.Column(db.Integer, nullable=False, default=0)  # garantía por comensal


class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    deposit_cents = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="CONFIRMED")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
