from app.models import Room
from tests.helpers import create_containers, create_items, create_rooms, assert_pagination_api_response

def test_get_rooms_paginated_api_returns_first_page(client, db_session, floor):
    create_rooms(db_session, floor.id, 30)
    resp = client.get("/rooms/?page=1")
    assert_pagination_api_response(resp, 200, 30, 1, 25)

def test_get_rooms_paginated_api_returns_second_page(client, db_session, floor):
    create_rooms(db_session, floor.id, 30)
    resp = client.get("/rooms/?page=2")
    assert_pagination_api_response(resp, 200, 30, 2, 5)

def test_get_rooms_paginated_api_empty_page(client, db_session, floor):
    create_rooms(db_session, floor.id, 10)
    resp = client.get("/rooms/?page=2")
    assert_pagination_api_response(resp, 200, 10, 2, 0)

def test_get_rooms_paginated_api_no_rooms(client):
    resp = client.get("/rooms/?page=1")
    assert_pagination_api_response(resp, 200, 0, 1, 0)

def test_get_room_api(client, db_session, floor):
    room = Room(name="Room B", floor_id=floor.id)
    db_session.add(room)
    db_session.commit()

    resp = client.get(f"/rooms/{room.id}")
    assert resp.status_code == 200

    payload = resp.json()
    assert payload["name"] == "Room B"
    assert payload["floor_id"] == floor.id
    assert payload["item_count"] == 0
    assert payload["container_count"] == 0

def test_get_room_api_includes_item_and_container_counts(client, db_session, floor):
    room = Room(name="Room B", floor_id=floor.id)
    db_session.add(room)
    db_session.commit()
    create_containers(db_session, room.id, 10)
    create_items(db_session, None, room.id, quantity=1, count=10)
    resp = client.get(f"/rooms/{room.id}")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["item_count"] == 10
    assert payload["container_count"] == 10
