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