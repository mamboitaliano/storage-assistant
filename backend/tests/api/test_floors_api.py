from app.models import Floor, Room


def test_list_floors_api(client, db_session):
    floor = Floor(name="First", floor_number=1)
    room = Room(name="Room A", floor=floor)

    db_session.add_all([floor, room])
    db_session.commit()

    response = client.get("/floors/")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["name"] == "First"
    assert payload[0]["room_count"] == 1


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
