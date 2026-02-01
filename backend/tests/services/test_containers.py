import os
import shutil
import tempfile

from app.models import Container
from app.schemas.containers import ContainerCreate, ContainerItemCreate
from app.services import containers as containers_service
from tests.helpers import create_containers, assert_pagination_service_response

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
    containers = create_containers(db_session, room.id, 1)
    
    result = containers_service.create_item_in_container(
        db_session, containers[0].id, ContainerItemCreate(name="Tape", quantity=3)
    )

    assert result is not None
    assert result.quantity == 3

def test_delete_container_removes(db_session, room):
    containers = create_containers(db_session, room.id, 1)

    resp = containers_service.delete_container(db_session, containers[0].id)
    assert resp["message"] == "Container deleted"
    assert db_session.query(Container).filter_by(id=containers[0].id).first() is None

# Pagination tests ----------------------------------------------------------------

def test_list_containers_paginated_returns_first_page(db_session, room):
    create_containers(db_session, room.id, 30)
    result = containers_service.list_containers_paginated(db_session, page=1, page_size=25)
    assert_pagination_service_response(result, 30, 1, 25, 25)

def test_list_containers_paginated_returns_second_page(db_session, room):
    create_containers(db_session, room.id, 30)
    result = containers_service.list_containers_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 30, 2, 25, 5)

def test_list_containers_paginated_returns_empty_page(db_session, room):
    create_containers(db_session, room.id, 10)
    result = containers_service.list_containers_paginated(db_session, page=2, page_size=25)
    assert_pagination_service_response(result, 10, 2, 25, 0)


# List all containers tests (for "Show all" dropdown) -----------------------------

def test_list_all_containers_returns_all_within_limit(db_session, room):
    """list_all_containers returns all containers when count is within limit"""
    create_containers(db_session, room.id, 50)
    
    containers, total, has_more = containers_service.list_all_containers(db_session, limit=200)
    
    assert len(containers) == 50
    assert total == 50
    assert has_more is False


def test_list_all_containers_returns_has_more_when_exceeds_limit(db_session, room):
    """list_all_containers returns has_more=True when total exceeds limit"""
    create_containers(db_session, room.id, 25)
    
    containers, total, has_more = containers_service.list_all_containers(db_session, limit=10)
    
    assert len(containers) == 10
    assert total == 25
    assert has_more is True


def test_list_all_containers_filters_by_room_ids(db_session, floor):
    """list_all_containers filters by room_ids when provided"""
    from app.models import Room
    
    room1 = Room(name="Room 1", floor_id=floor.id)
    room2 = Room(name="Room 2", floor_id=floor.id)
    db_session.add_all([room1, room2])
    db_session.commit()
    
    create_containers(db_session, room1.id, 5)
    create_containers(db_session, room2.id, 3)
    
    # Filter by room1 only
    containers, total, has_more = containers_service.list_all_containers(
        db_session, limit=200, room_ids=[room1.id]
    )
    
    assert len(containers) == 5
    assert total == 5
    assert has_more is False
    
    # Filter by both rooms
    containers, total, has_more = containers_service.list_all_containers(
        db_session, limit=200, room_ids=[room1.id, room2.id]
    )
    
    assert len(containers) == 8
    assert total == 8


def test_list_all_containers_empty(db_session):
    """list_all_containers returns empty list when no containers exist"""
    containers, total, has_more = containers_service.list_all_containers(db_session, limit=200)
    
    assert len(containers) == 0
    assert total == 0
    assert has_more is False
