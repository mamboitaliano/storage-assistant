import pytest
from app.models import Room, Item, Floor
from app.schemas.rooms import RoomCreate, RoomItemCreate
from app.services import rooms as rooms_service

@pytest.fixture
def floor(db_session):
    f = Floor(name="Test Floor", floor_number=1)
    db_session.add(f)
    db_session.commit()
    return f


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


def test_list_items_in_room_returns_paginated(db_session, floor):
    room = Room(name="Living", floor_id=floor.id)
    db_session.add(room)
    db_session.commit()

    for i in range(3):
        db_session.add(Item(name=f"Item {i}", room_id=room.id, quantity=1, container_id=None))
    db_session.commit()

    resp = rooms_service.list_items_in_room(db_session, room.id, page=1, page_size=2)
    
    assert resp is not None
    assert resp.total == 3
    assert len(resp.items) == 2  # page size limit
