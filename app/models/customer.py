from ..extensions import db

TIER_RANK = {"classic": 1, "gold": 2, "platinum": 3}


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    tier = db.Column(db.String(20), nullable=False, default="classic")


class Membership(db.Model):
    __tablename__ = "memberships"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), unique=True, nullable=False)
    tier = db.Column(db.String(20), nullable=False)
    valid_until = db.Column(db.Date, nullable=False)
    benefits = db.Column(db.Text, nullable=False, default="")  # separados por ';'
