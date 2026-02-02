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


# Filter API tests ----------------------------------------------------------------

def test_filter_containers_api_by_name(client, db_session, room):
    """API filters containers by name"""
    c1 = Container(name="Toolbox", room_id=room.id)
    c2 = Container(name="Storage Box", room_id=room.id)
    c3 = Container(name="Drawer", room_id=room.id)
    db_session.add_all([c1, c2, c3])
    db_session.commit()
    
    resp = client.get("/containers/?name=box")
    assert resp.status_code == 200
    
    payload = resp.json()
    assert payload["total"] == 2
    names = [c["name"] for c in payload["data"]]
    assert "Toolbox" in names
    assert "Storage Box" in names
    assert "Drawer" not in names


def test_filter_containers_api_by_rooms(client, db_session, floor):
    """API filters containers by rooms"""
    from app.models import Room
    
    room1 = Room(name="Garage", floor_id=floor.id)
    room2 = Room(name="Attic", floor_id=floor.id)
    db_session.add_all([room1, room2])
    db_session.commit()
    
    create_containers(db_session, room1.id, 3)
    create_containers(db_session, room2.id, 2)
    
    # Filter by room1
    resp = client.get(f"/containers/?rooms={room1.id}")
    assert resp.status_code == 200
    assert resp.json()["total"] == 3
    
    # Filter by both rooms
    resp = client.get(f"/containers/?rooms={room1.id},{room2.id}")
    assert resp.status_code == 200
    assert resp.json()["total"] == 5


# Room inclusion API tests --------------------------------------------------------

def test_get_containers_api_includes_room(client, db_session, room):
    """API returns nested room object for each container"""
    container = Container(name="Test Box", room_id=room.id)
    db_session.add(container)
    db_session.commit()
    
    resp = client.get("/containers/")
    assert resp.status_code == 200
    
    payload = resp.json()
    assert len(payload["data"]) == 1
    container_data = payload["data"][0]
    assert container_data["room"] is not None
    assert container_data["room"]["id"] == room.id
    assert container_data["room"]["name"] == room.name


def test_get_container_detail_api_includes_room(client, db_session, room):
    """API returns nested room object for container detail"""
    container = Container(name="Test Box", room_id=room.id)
    db_session.add(container)
    db_session.commit()
    
    resp = client.get(f"/containers/{container.id}")
    assert resp.status_code == 200
    
    payload = resp.json()
    assert payload["room"] is not None
    assert payload["room"]["id"] == room.id
    assert payload["room"]["name"] == room.name