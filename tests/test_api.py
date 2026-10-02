def test_health_returns_200(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok", "service": "bankpulse", "db": "up"}


def test_home_view_renders(client):
    assert b"BankPulse" in client.get("/").data


# HU-BP-01
def test_restaurants_filtered_by_capacity(client):
    r = client.get("/api/restaurants?date=2026-11-10&guests=8")
    names = [x["name"] for x in r.get_json()["results"]]
    assert "Casa Aurora" in names and "Mar Adentro" in names
    assert "Fuego Lento" not in names  # solo 6 asientos


def test_restaurants_invalid_date(client):
    assert client.get("/api/restaurants?date=hoy&guests=2").status_code == 400


# HU-BP-02
def test_reservation_created_and_capacity_consumed(client):
    body = {"customer_id": 1, "restaurant_id": 3, "date": "2026-11-10", "guests": 4}
    r = client.post("/api/reservations", json=body)
    assert r.status_code == 201
    assert r.get_json()["deposit_cents"] == 4000
    # quedan 2 asientos: otra reserva de 4 debe fallar con 409
    assert client.post("/api/reservations", json=body).status_code == 409


# HU-BP-04
def test_membership_found_and_missing(client):
    ok = client.get("/api/customers/1/membership")
    assert ok.status_code == 200 and ok.get_json()["tier"] == "platinum"
    assert client.get("/api/customers/3/membership").status_code == 404


# HU-BP-07
def test_events_eligibility_by_tier(client):
    gold = client.get("/api/events?customer_id=2&on=2026-10-05").get_json()["events"]
    classic = client.get("/api/events?customer_id=3&on=2026-10-05").get_json()["events"]
    concert = lambda evs: next(e for e in evs if e["id"] == 1)
    assert concert(gold)["eligible"] is True and concert(gold)["presale_open"] is True
    assert concert(classic)["eligible"] is False


# HU-BP-10
def test_split_equal_distributes_remainder(client):
    body = {"owner_id": 1, "description": "Cena", "total_cents": 10000, "mode": "equal",
            "members": [{"name": "A"}, {"name": "B"}, {"name": "C"}]}
    r = client.post("/api/splits", json=body)
    assert r.status_code == 201
    amounts = [s["amount_cents"] for s in r.get_json()["shares"]]
    assert sorted(amounts, reverse=True) == [3334, 3333, 3333] and sum(amounts) == 10000


def test_split_custom_must_sum_to_total(client):
    body = {"owner_id": 1, "description": "Cena", "total_cents": 10000, "mode": "custom",
            "members": [{"name": "A", "amount_cents": 4000}, {"name": "B", "amount_cents": 4000}]}
    assert client.post("/api/splits", json=body).status_code == 422
