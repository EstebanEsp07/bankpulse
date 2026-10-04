def _create(client, **overrides):
    body = {"owner_id": 1, "description": "Cena", "total_cents": 9000, "mode": "equal",
            "members": [{"name": "Ana"}, {"name": "Luis"}, {"name": "Eva"}]}
    body.update(overrides)
    return client.post("/api/splits", json=body)


def test_split_can_be_retrieved_with_summary(client):
    split_id = _create(client).get_json()["id"]
    data = client.get(f"/api/splits/{split_id}").get_json()
    assert data["pending_cents"] == 9000 and data["paid_cents"] == 0
    assert len(data["shares"]) == 3


def test_unknown_split_returns_404(client):
    assert client.get("/api/splits/999").status_code == 404


def test_duplicate_member_names_are_rejected(client):
    r = _create(client, members=[{"name": "Ana"}, {"name": " ana "}])
    assert r.status_code == 422


def test_split_requires_two_members(client):
    assert _create(client, members=[{"name": "Ana"}]).status_code == 422
