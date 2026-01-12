from app.models import Container, Floor, Item, Room

def test_list_containers_api(client, db_session):
    floor = Floor(name="First", floor_number=1)
    room = Room(name="Room A", floor=floor)
    container = Container(name="Bin", room=room, qr_code_path="/static/qr_codes/bin.png")
    item = Item(name="Widget", room=room, container=container, quantity=2)
    db_session.add_all([floor, room, container, item])
    db_session.commit()

    resp = client.get("/containers/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Bin"
    assert data[0]["room_id"] == room.id
    assert data[0]["item_count"] == 1


def test_get_container_api(client, db_session):
    floor = Floor(name="Second", floor_number=2)
    room = Room(name="Room B", floor=floor)
    container = Container(name="Crate", room=room, qr_code_path="/static/qr_codes/crate.png")
    item = Item(name="Cable", room=room, container=container, quantity=3)
    db_session.add_all([floor, room, container, item])
    db_session.commit()

    resp = client.get(f"/containers/{container.id}")
    assert resp.status_code == 200

    payload = resp.json()
    assert payload["name"] == "Crate"
    assert payload["room_id"] == room.id
    assert payload["item_count"] == 1
    assert payload["items"][0]["name"] == "Cable"
