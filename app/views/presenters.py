"""Vista (representación JSON): convierte entidades del Modelo en respuestas."""


def restaurant_view(restaurant, seats_left):
    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "cuisine": restaurant.cuisine,
        "city": restaurant.city,
        "seats_left": seats_left,
        "deposit_per_guest_cents": restaurant.deposit_cents,
    }


def reservation_view(r):
    return {
        "id": r.id,
        "restaurant_id": r.restaurant_id,
        "customer_id": r.customer_id,
        "date": r.date.isoformat(),
        "guests": r.guests,
        "deposit_cents": r.deposit_cents,
        "status": r.status,
    }


def membership_view(m):
    return {
        "customer_id": m.customer_id,
        "tier": m.tier,
        "valid_until": m.valid_until.isoformat(),
        "benefits": [b.strip() for b in m.benefits.split(";") if b.strip()],
    }


def event_view(item):
    e = item["event"]
    return {
        "id": e.id,
        "name": e.name,
        "venue": e.venue,
        "event_date": e.event_date.isoformat(),
        "presale_start": e.presale_start.isoformat(),
        "presale_end": e.presale_end.isoformat(),
        "min_tier": e.min_tier,
        "tickets_available": e.tickets_available,
        "per_customer_limit": e.per_customer_limit,
        "presale_open": item["presale_open"],
        "eligible": item["eligible"],
    }


def split_view(s):
    return {
        "id": s.id,
        "description": s.description,
        "total_cents": s.total_cents,
        "mode": s.mode,
        "shares": [
            {"member": sh.member_name, "amount_cents": sh.amount_cents, "status": sh.status}
            for sh in s.shares
        ],
    }
