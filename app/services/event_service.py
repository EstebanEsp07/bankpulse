from ..extensions import db
from ..models import Customer, Event
from ..models.customer import TIER_RANK
from .errors import DomainError


def list_events(customer_id, on_day, only_eligible=False, only_open=False):
    """HU-BP-07: eventos con ventana de preventa y elegibilidad por nivel."""
    customer = db.session.get(Customer, customer_id)
    if not customer:
        raise DomainError("Cliente no encontrado", 404)
    items = []
    for e in Event.query.order_by(Event.event_date).all():
        presale_open = e.presale_start <= on_day <= e.presale_end
        items.append(
            {
                "event": e,
                "presale_open": presale_open,
                "eligible": TIER_RANK[customer.tier] >= TIER_RANK[e.min_tier],
            }
        )
    if only_eligible:
        items = [i for i in items if i["eligible"]]
    if only_open:
        items = [i for i in items if i["presale_open"]]
    return items