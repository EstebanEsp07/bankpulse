from datetime import date
from flask import Blueprint, request
from ..services import event_service as svc
from ..services.errors import DomainError
from ..services.reservation_service import parse_date
from ..views.presenters import event_view

bp = Blueprint("events", __name__, url_prefix="/api")

@bp.get("/events")
def list_events():
    """HU-BP-07: eventos con ventana de preventa y elegibilidad por nivel."""
    customer_id = request.args.get("customer_id")
    if not customer_id:
        raise DomainError("customer_id es obligatorio", 400)
    try:
        customer_id = int(customer_id)
    except ValueError:
        raise DomainError("customer_id es obligatorio y debe ser entero", 400)
    on_day = parse_date(request.args["on"]) if "on" in request.args else date.today()
    only_eligible = request.args.get("only_eligible", "").lower() == "true"
    only_open = request.args.get("only_open", "").lower() == "true"
    items = svc.list_events(customer_id, on_day, only_eligible, only_open)
    return {"on": on_day.isoformat(), "events": [event_view(i) for i in items]}