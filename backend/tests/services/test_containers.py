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


# Filter tests --------------------------------------------------------------------

def test_filter_containers_by_name_returns_matching(db_session, room):
    """Filtering by name returns containers with matching names (case-insensitive)"""
    from app.models import Container
    
    c1 = Container(name="Toolbox", room_id=room.id)
    c2 = Container(name="Storage Box", room_id=room.id)
    c3 = Container(name="Kitchen Drawer", room_id=room.id)
    db_session.add_all([c1, c2, c3])
    db_session.commit()
    
    result = containers_service.list_containers_paginated(db_session, name="box")
    
    assert result.total == 2
    names = [c.name for c in result.data]
    assert "Toolbox" in names
    assert "Storage Box" in names
    assert "Kitchen Drawer" not in names


def test_filter_containers_by_rooms_returns_containers_in_rooms(db_session, floor):
    """Filtering by rooms returns only containers in those rooms"""
    from app.models import Room
    
    room1 = Room(name="Garage", floor_id=floor.id)
    room2 = Room(name="Attic", floor_id=floor.id)
    room3 = Room(name="Basement", floor_id=floor.id)
    db_session.add_all([room1, room2, room3])
    db_session.commit()
    
    create_containers(db_session, room1.id, 3)
    create_containers(db_session, room2.id, 2)
    create_containers(db_session, room3.id, 4)
    
    # Filter by room1 only
    result = containers_service.list_containers_paginated(db_session, rooms=[room1.id])
    assert result.total == 3
    
    # Filter by room1 and room2
    result = containers_service.list_containers_paginated(db_session, rooms=[room1.id, room2.id])
    assert result.total == 5


def test_filter_containers_by_name_and_rooms(db_session, floor):
    """Filtering by both name and rooms combines the filters"""
    from app.models import Room, Container
    
    room1 = Room(name="Garage", floor_id=floor.id)
    room2 = Room(name="Kitchen", floor_id=floor.id)
    db_session.add_all([room1, room2])
    db_session.commit()
    
    c1 = Container(name="Tool Bin", room_id=room1.id)
    c2 = Container(name="Storage Bin", room_id=room1.id)
    c3 = Container(name="Tool Drawer", room_id=room2.id)
    c4 = Container(name="Utensil Drawer", room_id=room2.id)
    db_session.add_all([c1, c2, c3, c4])
    db_session.commit()
    
    # Filter by "tool" in room1 only
    result = containers_service.list_containers_paginated(db_session, name="tool", rooms=[room1.id])
    
    assert result.total == 1
    assert result.data[0].name == "Tool Bin"


def test_filter_containers_with_pagination(db_session, room):
    """Filtering works correctly with pagination"""
    from app.models import Container
    
    # Create 30 containers, 15 with "Box" in name
    for i in range(15):
        db_session.add(Container(name=f"Box {i}", room_id=room.id))
    for i in range(15):
        db_session.add(Container(name=f"Drawer {i}", room_id=room.id))
    db_session.commit()
    
    # Filter by "box" with pagination
    result = containers_service.list_containers_paginated(db_session, page=1, page_size=10, name="box")
    
    assert result.total == 15
    assert len(result.data) == 10
    assert result.page == 1
    
    # Second page
    result = containers_service.list_containers_paginated(db_session, page=2, page_size=10, name="box")
    
    assert result.total == 15
    assert len(result.data) == 5
    assert result.page == 2


def test_filter_containers_no_matches_returns_empty(db_session, room):
    """Filtering with no matches returns empty results"""
    create_containers(db_session, room.id, 5)
    
    result = containers_service.list_containers_paginated(db_session, name="nonexistent")
    
    assert result.total == 0
    assert len(result.data) == 0


# Room inclusion tests ------------------------------------------------------------

def test_list_containers_paginated_includes_room(db_session, room):
    """list_containers_paginated includes nested room object"""
    create_containers(db_session, room.id, 1)
    
    result = containers_service.list_containers_paginated(db_session)
    
    assert len(result.data) == 1
    container = result.data[0]
    assert container.room is not None
    assert container.room.id == room.id
    assert container.room.name == room.name


def test_list_containers_paginated_room_is_none_when_no_room(db_session):
    """list_containers_paginated returns room=None when container has no room"""
    container = Container(name="Orphan Container", room_id=None)
    db_session.add(container)
    db_session.commit()
    
    result = containers_service.list_containers_paginated(db_session)
    
    assert len(result.data) == 1
    assert result.data[0].room is None


def test_get_container_detail_includes_room(db_session, room):
    """get_container_detail includes nested room object"""
    container = Container(name="Test Container", room_id=room.id)
    db_session.add(container)
    db_session.commit()
    
    result = containers_service.get_container_detail(db_session, container.id)
    
    assert result is not None
    assert result.room is not None
    assert result.room.id == room.id
    assert result.room.name == room.name


def test_get_container_detail_room_is_none_when_no_room(db_session):
    """get_container_detail returns room=None when container has no room"""
    container = Container(name="Orphan Container", room_id=None)
    db_session.add(container)
    db_session.commit()
    
    result = containers_service.get_container_detail(db_session, container.id)
    
    assert result is not None
    assert result.room is None


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
