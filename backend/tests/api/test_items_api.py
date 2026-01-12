from app.models import Floor, Room, Item

def test_update_item_api(client, db_session):
    floor = Floor(name="First", floor_number=1)
    room = Room(name="Room A", floor=floor)
    item = Item(name="Widget", room=room, container_id=None, quantity=1)
    db_session.add_all([floor, room, item])
    db_session.commit()

    resp = client.put(f"/items/{item.id}", json={"name": "Gadget", "quantity": 5})
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["name"] == "Gadget"
    assert data["quantity"] == 5


def test_delete_item_api(client, db_session):
    floor = Floor(name="Second", floor_number=2)
    room = Room(name="Room B", floor=floor)
    item = Item(name="Box", room=room, container_id=None, quantity=1)
    db_session.add_all([floor, room, item])
    db_session.commit()

    resp = client.delete(f"/items/{item.id}")
    assert resp.status_code == 200
    
    payload = resp.json()
    assert payload["message"] == "Item deleted"
