from app.models import Item
from app.schemas.items import ItemUpdate
from app.services import items as items_service

def test_update_item(db_session, room):
    item = Item(name="Widget", room_id=room.id, quantity=1, container_id=None)
    db_session.add(item)
    db_session.commit()

    updated = items_service.update_item(
        db_session,
        item.id,
        ItemUpdate(name="Gadget", quantity=5, room_id=room.id, container_id=None),
    )

    assert updated is not None
    assert updated.name == "Gadget"
    assert updated.quantity == 5
    assert updated.room_id == room.id
    assert updated.container_id is None

def test_delete_item_reduces_quantity(db_session, room):
    item = Item(name="Screws", room_id=room.id, quantity=10, container_id=None)
    db_session.add(item)
    db_session.commit()

    resp = items_service.delete_item(db_session, item.id, quantity=4)
    assert resp["message"] == "Item quantity reduced"
    db_session.refresh(item)
    assert item.quantity == 6

def test_delete_item_removes_when_no_quantity_given(db_session, room):
    item = Item(name="Box", room_id=room.id, quantity=1, container_id=None)
    db_session.add(item)
    db_session.commit()

    resp = items_service.delete_item(db_session, item.id)
    assert resp["message"] == "Item deleted"
    assert db_session.query(Item).filter_by(id=item.id).first() is None

# Pagination tests ------------------------------------------------------------

def create_items(db_session, room, count=30):
    for i in range(count):
        db_session.add(Item(name=f"Item {i}", room_id=room.id, quantity=1))
    db_session.commit();

def assert_pagination_result(result, total, page, page_size, data_length):
    assert result.total == total
    assert result.page == page
    assert result.pageSize == page_size
    assert len(result.data) == data_length

def test_get_items_paginated_returns_first_page(db_session, room):
    create_items(db_session, room, 30)
    result = items_service.get_items_paginated(db_session, page=1, page_size=25)
    assert_pagination_result(result, 30, 1, 25, 25)

def test_get_items_paginated_returns_second_page(db_session, room):
    create_items(db_session, room, 30)
    result = items_service.get_items_paginated(db_session, page=2, page_size=25)
    assert_pagination_result(result, 30, 2, 25, 5)

def test_get_items_paginated_empty_page(db_session, room):
    create_items(db_session, room, 10)
    result = items_service.get_items_paginated(db_session, page=2, page_size=25)
    assert_pagination_result(result, 10, 2, 25, 0)

def test_get_items_paginated_no_items(db_session):
    result = items_service.get_items_paginated(db_session, page=1, page_size=25)
    assert_pagination_result(result, 0, 1, 25, 0)