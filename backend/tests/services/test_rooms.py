from app.models import Room, Item
from app.schemas.rooms import RoomCreate, RoomItemCreate
from app.services import rooms as rooms_service
from tests.helpers import create_rooms, assert_pagination_service_response

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
    create_rooms(db_session, floor.id, 30)
    result = rooms_service.list_rooms_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 30, 1, 25, 25)

def test_list_rooms_paginated_returns_second_page(db_session, floor):
    create_rooms(db_session, floor.id, 30)
    result = rooms_service.list_rooms_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 30, 2, 25, 5)

def test_list_rooms_paginated_empty_page(db_session, floor):
    create_rooms(db_session, floor.id, 10)
    result = rooms_service.list_rooms_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 10, 2, 25, 0)

def test_list_rooms_paginated_no_rooms(db_session):
    result = rooms_service.list_rooms_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 0, 1, 25, 0)