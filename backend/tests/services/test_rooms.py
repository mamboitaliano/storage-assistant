from app.models import Room, Item, Container
from app.schemas.rooms import RoomCreate, RoomItemCreate
from app.services import rooms as rooms_service
from tests.helpers import create_items, create_containers, create_rooms, assert_pagination_service_response

def test_create_room(db_session, floor):
    data = RoomCreate(name="Office", floor_id=floor.id)
    resp = rooms_service.create_room(db_session, data)

    assert resp.name == "Office"
    assert resp.floor_id == floor.id

def test_create_item_in_room_increments_existing(db_session, floor):
    room = Room(name="Storage", floor_id=floor.id)
    item = Item(name="Lamp", room=room, quantity=1, container_id=None)
    db_session.add_all([room, item])
    db_session.commit()

    result = rooms_service.create_item_in_room(
        db_session, room.id, RoomItemCreate(name="lamp", quantity=2)
    )

    assert result is not None
    assert result.quantity == 3  # quantity increased

# Pagination tests ------------------------------------------------------------
def test_get_rooms_paginated_returns_first_page(db_session, floor):
    create_rooms(db_session, floor.id, 30)
    result = rooms_service.get_rooms_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 30, 1, 25, 25)

def test_get_rooms_paginated_returns_second_page(db_session, floor):
    create_rooms(db_session, floor.id, 30)
    result = rooms_service.get_rooms_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 30, 2, 25, 5)

def test_get_rooms_paginated_empty_page(db_session, floor):
    create_rooms(db_session, floor.id, 10)
    result = rooms_service.get_rooms_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 10, 2, 25, 0)

def test_get_rooms_paginated_no_rooms(db_session):
    result = rooms_service.get_rooms_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 0, 1, 25, 0)

# Nested item and container counts tests ---------------------------------------
def test_room_response_includes_item_and_container_counts(db_session, floor):
    room = Room(name="Test room", floor_id=floor.id)
    container = Container(name="Test container", room=room)
    item = Item(name="Test item", room=room, quantity=1)
    db_session.add_all([room, container, item])
    db_session.commit()
    result = rooms_service.get_room(db_session, room.id)
    assert result is not None
    assert result.item_count == 1
    assert result.container_count == 1

def test_get_rooms_paginated_includes_item_and_container_counts(db_session, floor):
    rooms = create_rooms(db_session, floor.id, 26)

    for room in rooms:
        create_containers(db_session, room.id, 10)
        create_items(db_session, None, room.id, quantity=1, count=10)
    
    result = rooms_service.get_rooms_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 26, 1, 25, 25)

    for room in result.data:
        assert room.item_count == 10, f"Room {room.id} has item_count={room.item_count}, expected 10"
        assert room.container_count == 10, f"Room {room.id} has container_count={room.container_count}, expected 10"
