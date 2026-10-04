def _book(client, **overrides):
    body = {"customer_id": 1, "restaurant_id": 1, "date": "2026-11-10", "guests": 2}
    body.update(overrides)
    return client.post("/api/reservations", json=body)


def test_reservation_rejects_more_than_12_guests(client):
    r = _book(client, guests=13)
    assert r.status_code == 422
    assert "12" in r.get_json()["error"]


def test_reservation_can_be_retrieved_after_creation(client):
    created = _book(client, guests=3).get_json()
    r = client.get(f"/api/reservations/{created['id']}")
    assert r.status_code == 200
    assert r.get_json()["guests"] == 3 and r.get_json()["status"] == "CONFIRMED"


def test_unknown_reservation_returns_404(client):
    assert client.get("/api/reservations/999").status_code == 404


def test_reservation_for_unknown_restaurant_returns_404(client):
    assert _book(client, restaurant_id=999).status_code == 404