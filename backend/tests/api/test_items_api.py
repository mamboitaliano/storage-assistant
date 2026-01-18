from app.models import Item

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

def create_items(db_session, room, count=30):
    for i in range(count):
        db_session.add(Item(name=f"Item {i}", room_id=room.id, quantity=1))
    db_session.commit();

def assert_pagination_result(response, status_code, total, page, data_length):
    data = response.json()
    assert response.status_code == status_code
    assert data["total"] == total
    assert data["page"] == page
    assert data["pageSize"] == 25
    assert len(data["data"]) == data_length

def test_get_items_paginated_api_returns_first_page(client, db_session, room):
    create_items(db_session, room, 30)
    resp = client.get("/items/?page=1")
    assert_pagination_result(resp, 200, 30, 1, 25)

def test_get_items_paginated_api_returns_second_page(client, db_session, room):
    create_items(db_session, room, 30)
    resp = client.get("/items/?page=2")
    assert_pagination_result(resp, 200, 30, 2, 5)

def test_get_items_paginated_api_empty_page(client, db_session, room):
    create_items(db_session, room, 10)
    resp = client.get("/items/?page=2")
    assert_pagination_result(resp, 200, 10, 2, 0)

def test_get_items_paginated_api_no_items(client):
    resp = client.get("/items/?page=1")
    assert_pagination_result(resp, 200, 0, 1, 0)