from datetime import datetime, timezone

from ..extensions import db


class ExpenseSplit(db.Model):
    __tablename__ = "expense_splits"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    total_cents = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.String(10), nullable=False)  # equal | custom
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    shares = db.relationship("SplitShare", backref="split", cascade="all, delete-orphan")


class SplitShare(db.Model):
    __tablename__ = "split_shares"
    id = db.Column(db.Integer, primary_key=True)
    split_id = db.Column(db.Integer, db.ForeignKey("expense_splits.id"), nullable=False)
    member_name = db.Column(db.String(120), nullable=False)
    amount_cents = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False, default="PENDING")  # PENDING | PAID
