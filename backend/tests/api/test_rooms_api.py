from app.models import Floor, Room

def test_list_rooms_api(client, db_session):
    floor = Floor(name="First", floor_number=1)
    room = Room(name="Room A", floor=floor)
    db_session.add_all([floor, room])
    db_session.commit()

    resp = client.get("/rooms/")
    assert resp.status_code == 200
    data = resp.json()

    assert isinstance(data, list)
    assert data[0]["name"] == "Room A"
    assert data[0]["floor_id"] == floor.id


def test_get_room_api(client, db_session):
    floor = Floor(name="Second", floor_number=2)
    room = Room(name="Room B", floor=floor)
    db_session.add_all([floor, room])
    db_session.commit()

    resp = client.get(f"/rooms/{room.id}")
    assert resp.status_code == 200

    payload = resp.json()
    assert payload["name"] == "Room B"
    assert payload["floor_id"] == floor.id
