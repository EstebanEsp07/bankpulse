def test_restaurants_can_be_filtered_by_city(client):
    r = client.get("/api/restaurants?date=2026-11-10&guests=4&city=Guayaquil")
    names = [x["name"] for x in r.get_json()["results"]]
    assert names == ["Fuego Lento"]


def test_city_filter_is_case_insensitive(client):
    r = client.get("/api/restaurants?date=2026-11-10&guests=2&city=quito")
    assert {x["name"] for x in r.get_json()["results"]} == {"Casa Aurora", "Mar Adentro"}


def test_unknown_city_returns_empty_list(client):
    r = client.get("/api/restaurants?date=2026-11-10&guests=2&city=Loja")
    assert r.status_code == 200 and r.get_json()["results"] == []
