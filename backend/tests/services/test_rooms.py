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

