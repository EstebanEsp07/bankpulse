from flask import Blueprint, render_template
from sqlalchemy import text

from ..extensions import db

bp = Blueprint("health", __name__)

ENDPOINTS = [
    {"method": "GET", "path": "/health", "story": "TEC", "desc": "estado del servicio y la BD"},
    {"method": "GET", "path": "/api/restaurants?date=AAAA-MM-DD&guests=N", "story": "HU-BP-01", "desc": "restaurantes con cupo"},
    {"method": "POST", "path": "/api/reservations", "story": "HU-BP-02", "desc": "reservar con garantía simulada"},
    {"method": "GET", "path": "/api/customers/<id>/membership", "story": "HU-BP-04", "desc": "consultar membresía"},
    {"method": "GET", "path": "/api/events?customer_id=<id>&on=AAAA-MM-DD", "story": "HU-BP-07", "desc": "eventos y elegibilidad"},
    {"method": "POST", "path": "/api/splits", "story": "HU-BP-10", "desc": "dividir un gasto"},
]


def _db_status():
    try:
        db.session.execute(text("SELECT 1"))
        return "up"
    except Exception:  # noqa: BLE001
        return "down"


@bp.get("/health")
def health():
    status = _db_status()
    code = 200 if status == "up" else 503
    return {"status": "ok" if code == 200 else "degraded", "service": "bankpulse", "db": status}, code


@bp.get("/")
def home():
    return render_template("home.html", service="bankpulse", db_status=_db_status(), endpoints=ENDPOINTS)
