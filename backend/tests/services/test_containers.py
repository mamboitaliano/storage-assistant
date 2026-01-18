import os
import shutil
import tempfile

from app.models import Container, Item
from app.schemas.containers import ContainerCreate, ContainerItemCreate
from app.services import containers as containers_service

def create_containers(db_session, room, count=1):
    for i in range(count):
        container = Container(name=f"Container {i}", room_id=room.id)
        db_session.add(container)
    db_session.commit()

def assert_pagination_response(result, total, page, data_length):
    assert result.total == total
    assert result.page == page
    assert result.pageSize == 25
    assert len(result.data) == data_length

def test_create_container_sets_qr_path(db_session, room):
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

def test_create_item_in_container_increments_existing(db_session, room):
    container = Container(name="Box", room_id=room.id)
    db_session.add(container)
    db_session.commit()
    item = Item(name="Tape", room_id=room.id, container_id=container.id, quantity=1)
    db_session.add(item)
    db_session.commit()
    
    result = containers_service.create_item_in_container(
        db_session, container.id, ContainerItemCreate(name="Tape", quantity=2)
    )

    assert result is not None
    assert result.quantity == 3

def test_delete_container_removes(db_session, room):
    container = Container(name="Crate", room_id=room.id)

    db_session.add(container)
    db_session.commit()

    resp = containers_service.delete_container(db_session, container.id)
    assert resp["message"] == "Container deleted"
    assert db_session.query(Container).filter_by(id=container.id).first() is None

# Pagination tests ----------------------------------------------------------------

def list_containers_paginated_returns_first_page(db_session, room):
    create_containers(db_session, room, 30)
    result = containers_service.list_containers_paginated(db_session, page=1, page_size=25)
    assert_pagination_response(result, 30, 1, 10)

def list_containers_paginated_returns_second_page(db_session, room):
    create_containers(db_session, room, 30)
    result = containers_service.list_containers_paginated(db_session, page=2, page_size=25)
    assert_pagination_response(result, 30, 2, 10)

def test_list_containers_paginated_empty_page(db_session, room):
    create_containers(db_session, room, 10)
    result = containers_service.list_containers_paginated(db_session, page=2, page_size=25)
    assert_pagination_response(result, 10, 2, 0)
