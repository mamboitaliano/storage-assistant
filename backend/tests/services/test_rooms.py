from app.models import Room, Item
from app.schemas.rooms import RoomCreate, RoomItemCreate
from app.services import rooms as rooms_service

def create_rooms(db_session, floor, count=30):
    for i in range(count):
        room = Room(name=f"Room {i}", floor_id=floor.id)
        db_session.add(room)
    db_session.commit()

def assert_pagination_result(result, total, page, page_size, data_length):
    assert result.total == total
    assert result.page == page
    assert result.pageSize == page_size
    assert len(result.data) == data_length

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
def test_list_rooms_paginated_returns_first_page(db_session, floor):
    create_rooms(db_session, floor, 30)
    result = rooms_service.list_rooms_paginated(db_session, page=1, page_size=25)
    assert_pagination_result(result, 30, 1, 25, 25)

def test_list_rooms_paginated_returns_second_page(db_session, floor):
    create_rooms(db_session, floor, 30)
    result = rooms_service.list_rooms_paginated(db_session, page=2, page_size=25)
    assert_pagination_result(result, 30, 2, 25, 5)

def test_list_rooms_paginated_empty_page(db_session, floor):
    create_rooms(db_session, floor, 10)
    result = rooms_service.list_rooms_paginated(db_session, page=2, page_size=25)
    assert_pagination_result(result, 10, 2, 25, 0)

def test_list_rooms_paginated_no_rooms(db_session):
    result = rooms_service.list_rooms_paginated(db_session, page=1, page_size=25)
    assert_pagination_result(result, 0, 1, 25, 0)