from app.models import Floor, Room
from tests.helpers import create_floors, assert_pagination_api_response

def test_get_floors_paginated_api_returns_first_page(client, db_session):
    create_floors(db_session, 30)
    resp = client.get("/floors/?page=1")
    assert_pagination_api_response(resp, 200, 30, 1, 25)

def test_get_floors_paginated_api_returns_second_page(client, db_session):
    create_floors(db_session, 30)
    resp = client.get("/floors/?page=2")
    assert_pagination_api_response(resp, 200, 30, 2, 5)

def test_get_floors_paginated_api_empty_page(client, db_session):
    create_floors(db_session, 10)
    resp = client.get("/floors/?page=2")
    assert_pagination_api_response(resp, 200, 10, 2, 0)

def test_get_floors_paginated_api_no_floors(client):
    resp = client.get("/floors/?page=1")
    assert_pagination_api_response(resp, 200, 0, 1, 0)

def test_get_floor_detail_api(client, db_session):
    floor = Floor(name="Second", floor_number=2)
    room = Room(name="Room B", floor=floor)

    db_session.add_all([floor, room])
    db_session.commit()

    response = client.get(f"/floors/{floor.id}")
    assert response.status_code == 200
    
    payload = response.json()
    assert payload["name"] == "Second"
    assert payload["room_count"] == 1
    assert payload["rooms"][0]["name"] == "Room B"

# Dropdown endpoint API tests -----------------------------------------------------

def test_get_floor_rooms_api(client, db_session):
    """GET /floors/{id}/rooms returns list of RoomOption"""
    floor = Floor(name="First", floor_number=1)
    room1 = Room(name="Living Room", floor=floor)
    room2 = Room(name="Kitchen", floor=floor)
    db_session.add_all([floor, room1, room2])
    db_session.commit()

    resp = client.get(f"/floors/{floor.id}/rooms")
    assert resp.status_code == 200
    
    data = resp.json()
    assert len(data) == 2
    # Verify lightweight response (id and name only)
    names = {r["name"] for r in data}
    assert "Living Room" in names
    assert "Kitchen" in names


def test_get_floor_rooms_api_empty(client, db_session):
    """GET /floors/{id}/rooms returns empty list when no rooms"""
    floor = Floor(name="Empty Floor", floor_number=1)
    db_session.add(floor)
    db_session.commit()

    resp = client.get(f"/floors/{floor.id}/rooms")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_floor_rooms_api_floor_not_found(client):
    """GET /floors/{id}/rooms returns 404 for non-existent floor"""
    resp = client.get("/floors/99999/rooms")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Floor not found"
