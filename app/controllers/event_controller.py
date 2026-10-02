from datetime import date

from flask import Blueprint, request

from ..services import event_service as svc
from ..services.errors import DomainError
from ..services.reservation_service import parse_date
from ..views.presenters import event_view

bp = Blueprint("events", __name__, url_prefix="/api")


@bp.get("/events")
def list_events():
    """HU-BP-07: GET /api/events?customer_id=<id>&on=AAAA-MM-DD"""
    try:
        customer_id = int(request.args.get("customer_id", ""))
    except ValueError:
        raise DomainError("customer_id es obligatorio y debe ser entero", 400)
    on_day = parse_date(request.args["on"]) if "on" in request.args else date.today()
    return {"on": on_day.isoformat(), "events": [event_view(i) for i in svc.list_events(customer_id, on_day)]}
