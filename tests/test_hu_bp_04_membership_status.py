def test_membership_is_active_before_expiration(client):
    data = client.get("/api/customers/1/membership?on=2027-12-01").get_json()
    assert data["active"] is True
    assert data["days_remaining"] == 30


def test_membership_is_inactive_after_expiration(client):
    data = client.get("/api/customers/1/membership?on=2028-01-01").get_json()
    assert data["active"] is False
    assert data["days_remaining"] == 0


def test_membership_invalid_date_returns_400(client):
    assert client.get("/api/customers/1/membership?on=mañana").status_code == 400


def test_membership_keeps_benefits_list(client):
    data = client.get("/api/customers/2/membership?on=2027-01-01").get_json()
    assert "Acceso a preventas" in data["benefits"]