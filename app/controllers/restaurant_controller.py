from flask import Blueprint, request

from ..services import reservation_service as svc
from ..services.errors import DomainError
from ..views.presenters import restaurant_view

bp = Blueprint("restaurants", __name__, url_prefix="/api")


@bp.get("/restaurants")
def list_restaurants():
    """HU-BP-01: GET /api/restaurants?date=AAAA-MM-DD&guests=N"""
    day = svc.parse_date(request.args.get("date"))
    try:
        guests = int(request.args.get("guests", "2"))
    except ValueError:
        raise DomainError("guests debe ser un entero", 400)
    found = svc.search_restaurants(day, guests)
    return {"date": day.isoformat(), "guests": guests, "results": [restaurant_view(r, s) for r, s in found]}
