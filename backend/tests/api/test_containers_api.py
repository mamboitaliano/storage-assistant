from app.models import Container
from tests.helpers import create_containers, assert_pagination_api_response

def test_get_containers_paginated_api_returns_first_page(client, db_session, room):
    create_containers(db_session, room.id, 30)
    resp = client.get("/containers/?page=1")
    assert_pagination_api_response(resp, 200, 30, 1, 25)

def test_get_containers_paginated_api_returns_second_page(client, db_session, room):
    create_containers(db_session, room.id, 30)
    resp = client.get("/containers/?page=2")
    assert_pagination_api_response(resp, 200, 30, 2, 5)

def test_get_containers_paginated_api_empty_page(client, db_session, room):
    create_containers(db_session, room.id, 10)
    resp = client.get("/containers/?page=2")
    assert_pagination_api_response(resp, 200, 10, 2, 0)

def test_get_containers_paginated_api_no_containers(client):
    resp = client.get("/containers/?page=1")
    assert_pagination_api_response(resp, 200, 0, 1, 0)

def test_get_container_api(client, db_session, room):
    container = Container(name="Crate", room_id=room.id, qr_code_path="/static/qr_codes/crate.png")
    db_session.add(container)
    db_session.commit()

    resp = client.get(f"/containers/{container.id}")
    assert resp.status_code == 200

    payload = resp.json()
    assert payload["name"] == "Crate"
    assert payload["room_id"] == room.id
    assert payload["qr_code_path"] == "/static/qr_codes/crate.png"
    assert payload["item_count"] == 0