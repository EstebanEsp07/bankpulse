from ..extensions import db
from ..models import Customer, ExpenseSplit, SplitShare
from .errors import DomainError


def compute_shares(total_cents, mode, members):
    """Calcula las partes. En modo equal el residuo se reparte en centavos."""
    if len(members) < 2:
        raise DomainError("Se requieren al menos 2 integrantes", 422)
    names = [m["name"].strip().lower() for m in members]
    if len(set(names)) != len(names):
        raise DomainError("Los nombres de los integrantes no pueden repetirse", 422)
    if mode == "equal":
        base, rest = divmod(total_cents, len(members))
        return [
            (m["name"], base + (1 if i < rest else 0)) for i, m in enumerate(members)
        ]
    if mode == "custom":
        amounts = [m.get("amount_cents") for m in members]
        if any(not isinstance(a, int) or a <= 0 for a in amounts):
            raise DomainError("Cada integrante requiere amount_cents entero positivo", 422)
        if sum(amounts) != total_cents:
            raise DomainError("La suma de las partes debe ser igual al total", 422)
        return [(m["name"], m["amount_cents"]) for m in members]
    raise DomainError("mode debe ser 'equal' o 'custom'", 400)


def create_split(owner_id, description, total_cents, mode, members):
    """HU-BP-10: crea una división de gasto con sus partes en estado PENDING."""
    if not db.session.get(Customer, owner_id):
        raise DomainError("Cliente no encontrado", 404)
    if not isinstance(total_cents, int) or total_cents <= 0:
        raise DomainError("total_cents debe ser un entero positivo", 422)
    shares = compute_shares(total_cents, mode, members)
    split = ExpenseSplit(
        owner_id=owner_id, description=description, total_cents=total_cents, mode=mode
    )
    split.shares = [SplitShare(member_name=n, amount_cents=a) for n, a in shares]
    db.session.add(split)
    db.session.commit()
    return split


def get_split(split_id):
    """HU-BP-10: recupera una división con el estado de cada parte."""
    split = db.session.get(ExpenseSplit, split_id)
    if not split:
        raise DomainError("División no encontrada", 404)
    return split