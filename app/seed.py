from datetime import date

from .extensions import db
from .models import Customer, Event, Membership, Restaurant


def seed_if_empty():
    """Datos semilla ficticios para demostrar el esqueleto (sin datos reales)."""
    if Customer.query.first():
        return
    db.session.add_all(
        [
            Customer(id=1, name="Ana Demo", email="ana@example.com", tier="platinum"),
            Customer(id=2, name="Luis Demo", email="luis@example.com", tier="gold"),
            Customer(id=3, name="Eva Demo", email="eva@example.com", tier="classic"),
            Membership(customer_id=1, tier="platinum", valid_until=date(2027, 12, 31),
                       benefits="Reservas prioritarias;Acceso a preventas;Credencial digital"),
            Membership(customer_id=2, tier="gold", valid_until=date(2027, 6, 30),
                       benefits="Reservas prioritarias;Acceso a preventas"),
            Restaurant(id=1, name="Casa Aurora", cuisine="Contemporánea", city="Quito", seats_per_day=20, deposit_cents=1500),
            Restaurant(id=2, name="Mar Adentro", cuisine="Mariscos", city="Quito", seats_per_day=10, deposit_cents=2000),
            Restaurant(id=3, name="Fuego Lento", cuisine="Parrilla", city="Guayaquil", seats_per_day=6, deposit_cents=1000),
            Event(id=1, name="Concierto Aurora (demo)", venue="Teatro Demo", event_date=date(2026, 12, 12),
                  presale_start=date(2026, 10, 1), presale_end=date(2026, 10, 15), min_tier="gold",
                  tickets_available=200, per_customer_limit=4),
            Event(id=2, name="Festival Gastronómico (demo)", venue="Parque Demo", event_date=date(2027, 1, 20),
                  presale_start=date(2026, 11, 1), presale_end=date(2026, 11, 20), min_tier="classic",
                  tickets_available=500, per_customer_limit=6),
        ]
    )
    db.session.commit()
