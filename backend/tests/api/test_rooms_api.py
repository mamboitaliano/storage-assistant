from app.models import Room
from tests.services.test_rooms import create_rooms

def assert_pagination_result(response, status_code, total, page, data_length):
    data = response.json()
    assert response.status_code == status_code
    assert data["total"] == total
    assert data["page"] == page
    assert data["pageSize"] == 25
    assert len(data["data"]) == data_length

def test_get_rooms_paginated_api_returns_first_page(client, db_session, floor):
    create_rooms(db_session, floor, 30)
    resp = client.get("/rooms/?page=1")
    assert_pagination_result(resp, 200, 30, 1, 25)

def test_get_rooms_paginated_api_returns_second_page(client, db_session, floor):
    create_rooms(db_session, floor, 30)
    resp = client.get("/rooms/?page=2")
    assert_pagination_result(resp, 200, 30, 2, 5)

def test_get_rooms_paginated_api_empty_page(client, db_session, floor):
    create_rooms(db_session, floor, 10)
    resp = client.get("/rooms/?page=2")
    assert_pagination_result(resp, 200, 10, 2, 0)

def test_get_rooms_paginated_api_no_rooms(client):
    resp = client.get("/rooms/?page=1")
    assert_pagination_result(resp, 200, 0, 1, 0)

def test_get_room_api(client, db_session, floor):
    room = Room(name="Room B", floor_id=floor.id)
    db_session.add(room)
    db_session.commit()

    resp = client.get(f"/rooms/{room.id}")
    assert resp.status_code == 200

    payload = resp.json()
    assert payload["name"] == "Room B"
    assert payload["floor_id"] == floor.id
