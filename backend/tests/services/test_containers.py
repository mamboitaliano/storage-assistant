import os
import shutil
import tempfile

import pytest

from app.models import Container, Floor, Item, Room
from app.schemas.containers import ContainerCreate, ContainerItemCreate
from app.services import containers as containers_service


@pytest.fixture
def floor(db_session):
    f = Floor(name="Test Floor", floor_number=1)
    db_session.add(f)
    db_session.commit()
    return f


def test_create_container_sets_qr_path(db_session, floor):
    room = Room(name="Hall", floor_id=floor.id)
    db_session.add(room)
    db_session.commit()

    tmpdir = tempfile.mkdtemp()
    original_dir = containers_service.QR_DIR

    try:
        containers_service.QR_DIR = tmpdir
        resp = containers_service.create_container(db_session, ContainerCreate(name="Bin", room_id=room.id))

        assert resp.name == "Bin"
        assert resp.room_id == room.id
        assert resp.qr_code_path is not None

        filename = os.path.basename(resp.qr_code_path)
        assert os.path.exists(os.path.join(tmpdir, filename))
    finally:
        containers_service.QR_DIR = original_dir
        shutil.rmtree(tmpdir, ignore_errors=True)


def test_create_item_in_container_increments_existing(db_session, floor):
    room = Room(name="Storage", floor_id=floor.id)
    container = Container(name="Box", room=room)
    item = Item(name="Tape", room=room, container=container, quantity=1)

    db_session.add_all([room, container, item])
    db_session.commit()

    result = containers_service.create_item_in_container(
        db_session, container.id, ContainerItemCreate(name="Tape", quantity=2)
    )

    assert result is not None
    assert result.quantity == 3


def test_delete_container_removes(db_session, floor):
    room = Room(name="Garage", floor_id=floor.id)
    container = Container(name="Crate", room=room)

    db_session.add_all([room, container])
    db_session.commit()

    resp = containers_service.delete_container(db_session, container.id)
    assert resp["message"] == "Container deleted"
    assert db_session.query(Container).filter_by(id=container.id).first() is None
