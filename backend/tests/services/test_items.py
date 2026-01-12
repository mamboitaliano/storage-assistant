import pytest
from app.models import Item, Room, Floor
from app.schemas.items import ItemUpdate
from app.services import items as items_service

@pytest.fixture
def room(db_session):
    f = Floor(name="Test Floor", floor_number=1)
    db_session.add(f)
    db_session.commit()

    r = Room(name="Test Room", floor_id=f.id)
    db_session.add(r)
    db_session.commit()
    return r


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
