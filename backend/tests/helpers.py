"""Shared test helper functions"""

from app.models import Floor, Room, Container, Item

def assert_pagination_api_response(response, status_code, total, page, data_length):
    """Assert that the API response is a valid pagination response"""
    data = response.json()
    assert response.status_code == status_code
    assert data["total"] == total
    assert data["page"] == page
    assert data["pageSize"] == 25
    assert len(data["data"]) == data_length

def assert_pagination_service_response(result, total, page, page_size, data_length):
    """Assert that the service response is a valid pagination response"""
    assert result.total == total
    assert result.page == page
    assert result.pageSize == page_size
    assert len(result.data) == data_length

def create_floors(db_session, count=30):
    """Create test floors"""
    floors = [Floor(name=f"Floor {i}", floor_number=i) for i in range(count)]
    db_session.add_all(floors)
    db_session.commit()
    return floors

def create_rooms(db_session, floor_id, count=30):
    """Create test rooms"""
    rooms = [Room(name=f"Room {i}", floor_id=floor_id) for i in range(count)]
    db_session.add_all(rooms)
    db_session.commit()
    return rooms

def create_containers(db_session, room_id, count=30):
    """Create test containers"""
    containers = [Container(name=f"Container {i}", room_id=room_id, qr_code_path="/static/qr_codes/bin.png") for i in range(count)]
    db_session.add_all(containers)
    db_session.commit()
    return containers

def create_items(db_session, container_id, room_id, quantity=1, count=30):
    """Create test items"""
    items = [Item(name=f"Item {i}", container_id=container_id, room_id=room_id, quantity=quantity) for i in range(count)]
    db_session.add_all(items)
    db_session.commit()
    return items