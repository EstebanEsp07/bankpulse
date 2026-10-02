from ..extensions import db


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    venue = db.Column(db.String(120), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    presale_start = db.Column(db.Date, nullable=False)
    presale_end = db.Column(db.Date, nullable=False)
    min_tier = db.Column(db.String(20), nullable=False, default="classic")
    tickets_available = db.Column(db.Integer, nullable=False)
    per_customer_limit = db.Column(db.Integer, nullable=False, default=4)
