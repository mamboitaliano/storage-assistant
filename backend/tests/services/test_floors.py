from app.models import Room
from app.services import floors as floors_service
from tests.helpers import create_floors, create_rooms, create_containers, create_items, assert_pagination_service_response

def test_list_floors_paginated_includes_room_counts(db_session):
    floors = create_floors(db_session,1)
    create_rooms(db_session, floors[0].id, 2)

    result = floors_service.list_floors_paginated(db_session, page=1, page_size=25)
    
    assert len(result.data) == 1
    assert result.data[0].room_count == 2

def test_get_floor_detail_with_counts(db_session):
    floors = create_floors(db_session,1)
    rooms = create_rooms(db_session, floors[0].id, 1)
    containers = create_containers(db_session, rooms[0].id, 1)
    items = create_items(db_session, containers[0].id, rooms[0].id, quantity=1, count=1)

    result = floors_service.get_floor_detail(db_session, floors[0].id)

    assert result is not None
    assert result.room_count == 1
    assert len(result.rooms or []) == 1

    room_resp = result.rooms[0]
    assert room_resp.container_count == 1
    assert room_resp.item_count == 1

# Pagination tests ------------------------------------------------------------
def test_list_floors_paginated_returns_first_page(db_session):
    create_floors(db_session, 30)
    result = floors_service.list_floors_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 30, 1, 25, 25)

def test_list_floors_paginated_returns_second_page(db_session):
    create_floors(db_session, 30)
    result = floors_service.list_floors_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 30, 2, 25, 5)

def test_list_floors_paginated_empty_page(db_session):
    create_floors(db_session, 10)
    result = floors_service.list_floors_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 10, 2, 25, 0)

def test_list_floors_paginated_no_floors(db_session):
    result = floors_service.list_floors_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 0, 1, 25, 0)