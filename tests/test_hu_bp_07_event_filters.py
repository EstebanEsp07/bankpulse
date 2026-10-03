def _ids(resp):
    return [e["id"] for e in resp.get_json()["events"]]


def test_only_open_returns_events_with_active_presale(client):
    r = client.get("/api/events?customer_id=2&on=2026-10-05&only_open=true")
    assert _ids(r) == [1]


def test_only_eligible_hides_events_above_customer_tier(client):
    r = client.get("/api/events?customer_id=3&on=2026-11-05&only_eligible=true")
    assert _ids(r) == [2]


def test_filters_combine(client):
    r = client.get("/api/events?customer_id=3&on=2026-10-05&only_eligible=true&only_open=true")
    assert _ids(r) == []


def test_without_filters_returns_all_events(client):
    r = client.get("/api/events?customer_id=1&on=2026-10-05")
    assert _ids(r) == [1, 2]