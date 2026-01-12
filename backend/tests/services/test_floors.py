from app.models import Container, Floor, Item, Room
from app.services import floors as floors_service

def test_list_floors_with_counts(db_session):
    floor = Floor(name="First", floor_number=1)
    room1 = Room(name="Room A", floor=floor)
    room2 = Room(name="Room B", floor=floor)

    db_session.add_all([floor, room1, room2])
    db_session.commit()

    result = floors_service.list_floors_with_counts(db_session)

    assert len(result) == 1
    
    floor_response = result[0] 
    assert floor_response.name == "First"
    assert floor_response.room_count == 2


def test_get_floor_detail_with_counts(db_session):
    floor = Floor(name="Second", floor_number=2)
    room = Room(name="Storage", floor=floor)
    container = Container(name="Bin", room=room)
    item = Item(name="Hammer", room=room, container=container, quantity=1)

    db_session.add_all([floor, room, container, item])
    db_session.commit()

    result = floors_service.get_floor_detail(db_session, floor.id)

    assert result is not None
    assert result.room_count == 1
    assert len(result.rooms or []) == 1

    room_resp = result.rooms[0]
    assert room_resp.name == "Storage"
    assert room_resp.container_count == 1
    assert room_resp.item_count == 1
