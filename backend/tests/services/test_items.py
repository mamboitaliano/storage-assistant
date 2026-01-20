from app.models import Item
from app.schemas.items import ItemUpdate
from app.services import items as items_service
from tests.helpers import create_items, assert_pagination_service_response

def test_update_item(db_session, room):
    items = create_items(db_session, None, room.id, 1)
    updated = items_service.update_item(
        db_session,
        items[0].id,
        ItemUpdate(name="Gadget", quantity=5, room_id=room.id, container_id=None),
    )

    assert updated is not None
    assert updated.name == "Gadget"
    assert updated.quantity == 5
    assert updated.room_id == room.id
    assert updated.container_id is None

def test_delete_item_reduces_quantity(db_session, room):
    items = create_items(db_session, None, room.id, quantity=10, count=1)

    resp = items_service.delete_item(db_session, items[0].id, quantity=4)
    assert resp["message"] == "Item quantity reduced"
    db_session.refresh(items[0])
    assert items[0].quantity == 6

def test_delete_item_removes_when_no_quantity_given(db_session, room):
    items = create_items(db_session, None, room.id, quantity=1, count=1)
    resp = items_service.delete_item(db_session, items[0].id)
    assert resp["message"] == "Item deleted"
    assert db_session.query(Item).filter_by(id=items[0].id).first() is None

# Pagination tests ------------------------------------------------------------

def test_get_items_paginated_returns_first_page(db_session, room):
    create_items(db_session, None, room.id, quantity=1, count=30)
    result = items_service.get_items_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 30, 1, 25, 25)

def test_get_items_paginated_returns_second_page(db_session, room):
    create_items(db_session, None, room.id, quantity=1, count=30)
    result = items_service.get_items_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 30, 2, 25, 5)

def test_get_items_paginated_empty_page(db_session, room):
    create_items(db_session, None, room.id, quantity=1, count=10)
    result = items_service.get_items_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 10, 2, 25, 0)

def test_get_items_paginated_no_items(db_session):
    result = items_service.get_items_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 0, 1, 25, 0)

# Nested relationship tests -------------------------------------------------------

def test_get_items_paginated_includes_room(db_session, room):
    """Items should include nested room with id and name"""
    create_items(db_session, None, room.id, quantity=1, count=1)
    result = items_service.get_items_paginated(db_session, page=1, page_size=25)
    
    assert len(result.data) == 1
    item = result.data[0]
    assert item.room is not None
    assert item.room.id == room.id
    assert item.room.name == room.name

def test_get_items_paginated_includes_container_when_present(db_session, room, container):
    """Items in a container should include nested container with id and name"""
    create_items(db_session, container.id, room.id, quantity=1, count=1)
    result = items_service.get_items_paginated(db_session, page=1, page_size=25)
    
    assert len(result.data) == 1
    item = result.data[0]
    assert item.container is not None
    assert item.container.id == container.id
    assert item.container.name == container.name

def test_get_items_paginated_container_is_none_when_not_in_container(db_session, room):
    """Items not in a container should have container as None"""
    create_items(db_session, None, room.id, quantity=1, count=1)
    result = items_service.get_items_paginated(db_session, page=1, page_size=25)
    
    assert len(result.data) == 1
    item = result.data[0]
    assert item.container is None