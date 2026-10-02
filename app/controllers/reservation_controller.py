from flask import Blueprint, request

from ..services import reservation_service as svc
from ..services.errors import DomainError
from ..views.presenters import reservation_view

bp = Blueprint("reservations", __name__, url_prefix="/api")


@bp.post("/reservations")
def create_reservation():
    """HU-BP-02: POST /api/reservations {customer_id, restaurant_id, date, guests}"""
    data = request.get_json(silent=True) or {}
    try:
        customer_id = int(data["customer_id"])
        restaurant_id = int(data["restaurant_id"])
        guests = int(data["guests"])
    except (KeyError, TypeError, ValueError):
        raise DomainError("Faltan campos o son inválidos: customer_id, restaurant_id, date, guests", 400)
    day = svc.parse_date(data.get("date"))
    reservation = svc.create_reservation(customer_id, restaurant_id, day, guests)
    return reservation_view(reservation), 201
