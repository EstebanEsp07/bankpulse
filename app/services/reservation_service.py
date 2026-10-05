from datetime import date

from sqlalchemy import func

from ..extensions import db
from ..models import Customer, Reservation, Restaurant
from .errors import DomainError

MAX_GUESTS_PER_RESERVATION = 12


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise DomainError("Fecha inválida; use formato AAAA-MM-DD", 400)


def available_seats(restaurant, day):
    booked = (
        db.session.query(func.coalesce(func.sum(Reservation.guests), 0))
        .filter_by(restaurant_id=restaurant.id, date=day, status="CONFIRMED")
        .scalar()
    )
    return restaurant.seats_per_day - int(booked)


def search_restaurants(day, guests, city=None):
    """HU-BP-01: restaurantes con cupo suficiente para la fecha y comensales."""
    if guests < 1:
        raise DomainError("El número de comensales debe ser al menos 1", 400)
    result = []
    for r in Restaurant.query.order_by(Restaurant.name).all():
        if city and r.city.lower() != city.lower():
            continue
        seats = available_seats(r, day)
        if seats >= guests:
            result.append((r, seats))
    return result


def create_reservation(customer_id, restaurant_id, day, guests):
    """HU-BP-02: reserva con garantía simulada (sin pasarela real de pagos)."""
    if guests < 1:
        raise DomainError("El número de comensales debe ser al menos 1", 400)
    if guests > MAX_GUESTS_PER_RESERVATION:
        raise DomainError(
            f"Una reserva admite como máximo {MAX_GUESTS_PER_RESERVATION} comensales", 422
        )
    if not db.session.get(Customer, customer_id):
        raise DomainError("Cliente no encontrado", 404)
    restaurant = db.session.get(Restaurant, restaurant_id)
    if not restaurant:
        raise DomainError("Restaurante no encontrado", 404)
    if available_seats(restaurant, day) < guests:
        raise DomainError("No hay cupo suficiente para la fecha solicitada", 409)
    reservation = Reservation(
        restaurant_id=restaurant.id,
        customer_id=customer_id,
        date=day,
        guests=guests,
        deposit_cents=restaurant.deposit_cents * guests,
    )
    db.session.add(reservation)
    db.session.commit()
    return reservation
    
def get_reservation(reservation_id):
    """HU-BP-02: recupera una reserva para mostrar su confirmación."""
    reservation = db.session.get(Reservation, reservation_id)
    if not reservation:
        raise DomainError("Reserva no encontrada", 404)
    return reservation