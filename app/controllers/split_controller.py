from flask import Blueprint, request

from ..services import split_service as svc
from ..services.errors import DomainError
from ..views.presenters import split_view

bp = Blueprint("splits", __name__, url_prefix="/api")


@bp.post("/splits")
def create_split():
    """HU-BP-10: POST /api/splits {owner_id, description, total_cents, mode, members[]}"""
    data = request.get_json(silent=True) or {}
    try:
        owner_id = int(data["owner_id"])
        description = str(data["description"])
        members = list(data["members"])
        mode = data["mode"]
        total_cents = data["total_cents"]
    except (KeyError, TypeError, ValueError):
        raise DomainError("Campos obligatorios: owner_id, description, total_cents, mode, members", 400)
    if not all(isinstance(m, dict) and m.get("name") for m in members):
        raise DomainError("Cada integrante requiere 'name'", 422)
    return split_view(svc.create_split(owner_id, description, total_cents, mode, members)), 201


@bp.get("/splits/<int:split_id>")
def get_split(split_id):
    """HU-BP-10: GET /api/splits/<id> con resumen de pagado y pendiente."""
    split = svc.get_split(split_id)
    view = split_view(split)
    view["paid_cents"] = sum(s.amount_cents for s in split.shares if s.status == "PAID")
    view["pending_cents"] = sum(s.amount_cents for s in split.shares if s.status == "PENDING")
    return view