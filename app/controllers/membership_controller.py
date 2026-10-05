from datetime import date

from flask import Blueprint, request

from ..extensions import db
from ..models import Customer, Membership
from ..services.errors import DomainError
from ..services.reservation_service import parse_date
from ..views.presenters import membership_view

bp = Blueprint("membership", __name__, url_prefix="/api")


@bp.get("/customers/<int:customer_id>/membership")
def get_membership(customer_id):
    """HU-BP-04: nivel, vigencia y beneficios de la membresía."""
    if not db.session.get(Customer, customer_id):
        raise DomainError("Cliente no encontrado", 404)
    membership = Membership.query.filter_by(customer_id=customer_id).first()
    if not membership:
        raise DomainError("El cliente no tiene membresía activa", 404)
    on_day = parse_date(request.args["on"]) if "on" in request.args else date.today()
    return membership_view(membership, on_day)