from app.models import Item
from tests.helpers import create_items, assert_pagination_api_response

# Create item API tests -----------------------------------------------------------

def test_create_item_api_with_room_only(client, room):
    """POST /items creates item with room and returns 201 with nested room"""
    resp = client.post("/items/", json={
        "name": "Screwdriver",
        "quantity": 2,
        "room_id": room.id
    })
    
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Screwdriver"
    assert data["quantity"] == 2
    assert data["room_id"] == room.id
    assert data["room"]["id"] == room.id
    assert data["room"]["name"] == room.name
    assert data["container_id"] is None
    assert data["container"] is None


def test_create_item_api_with_room_and_container(client, room, container):
    """POST /items creates item with room and container"""
    resp = client.post("/items/", json={
        "name": "Hammer",
        "quantity": 1,
        "room_id": room.id,
        "container_id": container.id
    })
    
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Hammer"
    assert data["room_id"] == room.id
    assert data["room"]["id"] == room.id
    assert data["container_id"] == container.id
    assert data["container"]["id"] == container.id
    assert data["container"]["name"] == container.name


def test_create_item_api_missing_room_id(client):
    """POST /items without room_id returns 422 validation error"""
    resp = client.post("/items/", json={
        "name": "Widget",
        "quantity": 1
    })
    
    assert resp.status_code == 422


def test_create_item_api_room_not_found(client):
    """POST /items with invalid room_id returns 404"""
    resp = client.post("/items/", json={
        "name": "Widget",
        "quantity": 1,
        "room_id": 99999
    })
    
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Room not found"


def test_create_item_api_container_not_found(client, room):
    """POST /items with invalid container_id returns 404"""
    resp = client.post("/items/", json={
        "name": "Widget",
        "quantity": 1,
        "room_id": room.id,
        "container_id": 99999
    })
    
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Container not found"


# Update item API tests -----------------------------------------------------------

def test_update_item_api(client, db_session, room):
    item = Item(name="Widget", room_id=room.id, container_id=None, quantity=1)
    db_session.add(item)
    db_session.commit()

    resp = client.put(f"/items/{item.id}", json={"name": "Gadget", "quantity": 5})
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["name"] == "Gadget"
    assert data["quantity"] == 5

def test_delete_item_api(client, db_session, room):
    item = Item(name="Box", room_id=room.id, container_id=None, quantity=1)
    db_session.add(item)
    db_session.commit()

    resp = client.delete(f"/items/{item.id}")
    assert resp.status_code == 200

    payload = resp.json()
    assert payload["message"] == "Item deleted"

# Pagination tests ------------------------------------------------------------

def test_get_items_paginated_api_returns_first_page(client, db_session, room):
    create_items(db_session, None, room.id, quantity=1, count=30)
    resp = client.get("/items/?page=1")
    assert_pagination_api_response(resp, 200, 30, 1, 25)

def test_get_items_paginated_api_returns_second_page(client, db_session, room):
    create_items(db_session, None, room.id, quantity=1, count=30)
    resp = client.get("/items/?page=2")
    assert_pagination_api_response(resp, 200, 30, 2, 5)

def test_get_items_paginated_api_empty_page(client, db_session, room):
    create_items(db_session, None, room.id, quantity=1, count=10)
    resp = client.get("/items/?page=2")
    assert_pagination_api_response(resp, 200, 10, 2, 0)

def test_get_items_paginated_api_no_items(client):
    resp = client.get("/items/?page=1")
    assert_pagination_api_response(resp, 200, 0, 1, 0)


# Filter API tests ----------------------------------------------------------------

def test_filter_items_api_by_name(client, db_session, room):
    """GET /items?name=X returns items matching name"""
    from app.models import Item
    db_session.add_all([
        Item(name="Screwdriver", room_id=room.id, quantity=1),
        Item(name="Hammer", room_id=room.id, quantity=1),
        Item(name="Phillips Screwdriver", room_id=room.id, quantity=1),
    ])
    db_session.commit()
    
    resp = client.get("/items/?name=screwdriver")
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    names = [item["name"] for item in data["data"]]
    assert "Screwdriver" in names
    assert "Phillips Screwdriver" in names


def test_filter_items_api_by_rooms(client, db_session, floor):
    """GET /items?rooms=1,2 returns items in specified rooms"""
    from app.models import Room, Item
    room1 = Room(name="Kitchen", floor_id=floor.id)
    room2 = Room(name="Garage", floor_id=floor.id)
    room3 = Room(name="Bedroom", floor_id=floor.id)
    db_session.add_all([room1, room2, room3])
    db_session.commit()
    
    db_session.add_all([
        Item(name="Spatula", room_id=room1.id, quantity=1),
        Item(name="Wrench", room_id=room2.id, quantity=1),
        Item(name="Pillow", room_id=room3.id, quantity=1),
    ])
    db_session.commit()
    
    resp = client.get(f"/items/?rooms={room1.id},{room2.id}")
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    names = [item["name"] for item in data["data"]]
    assert "Spatula" in names
    assert "Wrench" in names


def test_filter_items_api_by_containers(client, db_session, room):
    """GET /items?containers=1 returns items in specified containers"""
    from app.models import Container, Item
    container1 = Container(name="Toolbox", room_id=room.id)
    container2 = Container(name="Drawer", room_id=room.id)
    db_session.add_all([container1, container2])
    db_session.commit()
    
    db_session.add_all([
        Item(name="Hammer", room_id=room.id, container_id=container1.id, quantity=1),
        Item(name="Scissors", room_id=room.id, container_id=container2.id, quantity=1),
    ])
    db_session.commit()
    
    resp = client.get(f"/items/?containers={container1.id}")
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["data"][0]["name"] == "Hammer"


def test_filter_items_api_by_name_and_rooms(client, db_session, floor):
    """GET /items?name=X&rooms=1 returns matching items in specified rooms"""
    from app.models import Room, Item
    room1 = Room(name="Kitchen", floor_id=floor.id)
    room2 = Room(name="Garage", floor_id=floor.id)
    db_session.add_all([room1, room2])
    db_session.commit()
    
    db_session.add_all([
        Item(name="Red Screwdriver", room_id=room1.id, quantity=1),
        Item(name="Blue Screwdriver", room_id=room2.id, quantity=1),
    ])
    db_session.commit()
    
    resp = client.get(f"/items/?name=screwdriver&rooms={room1.id}")
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["data"][0]["name"] == "Red Screwdriver"


def test_filter_items_api_container_room_mismatch_returns_400(client, db_session, floor):
    """GET /items?rooms=1&containers=2 returns 400 when container not in room"""
    from app.models import Room, Container
    room1 = Room(name="Kitchen", floor_id=floor.id)
    room2 = Room(name="Garage", floor_id=floor.id)
    db_session.add_all([room1, room2])
    db_session.commit()
    
    container_in_room2 = Container(name="Toolbox", room_id=room2.id)
    db_session.add(container_in_room2)
    db_session.commit()
    
    resp = client.get(f"/items/?rooms={room1.id}&containers={container_in_room2.id}")
    
    assert resp.status_code == 400
    assert resp.json()["detail"] == "One or more containers do not belong to the specified rooms"