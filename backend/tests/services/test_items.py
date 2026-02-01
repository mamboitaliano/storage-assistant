from app.models import Item
from app.schemas.items import ItemCreate, ItemUpdate
from app.services import items as items_service
from tests.helpers import create_items, assert_pagination_service_response

# Create item tests ---------------------------------------------------------------

def test_create_item_with_room_only(db_session, room):
    """Item can be created with just a room assignment"""
    data = ItemCreate(name="Screwdriver", quantity=2, room_id=room.id)
    item, error = items_service.create_item(db_session, data)
    
    assert error is None
    assert item is not None
    assert item.name == "Screwdriver"
    assert item.quantity == 2
    assert item.room_id == room.id
    assert item.room.id == room.id
    assert item.room.name == room.name
    assert item.container_id is None
    assert item.container is None


def test_create_item_with_room_and_container(db_session, room, container):
    """Item can be created with room and container assignment"""
    data = ItemCreate(name="Hammer", quantity=1, room_id=room.id, container_id=container.id)
    item, error = items_service.create_item(db_session, data)
    
    assert error is None
    assert item is not None
    assert item.name == "Hammer"
    assert item.room_id == room.id
    assert item.room.id == room.id
    assert item.container_id == container.id
    assert item.container.id == container.id
    assert item.container.name == container.name


def test_create_item_room_not_found(db_session):
    """Returns error when room doesn't exist"""
    data = ItemCreate(name="Widget", quantity=1, room_id=99999)
    item, error = items_service.create_item(db_session, data)
    
    assert item is None
    assert error == "room_not_found"


def test_create_item_container_not_found(db_session, room):
    """Returns error when container doesn't exist"""
    data = ItemCreate(name="Widget", quantity=1, room_id=room.id, container_id=99999)
    item, error = items_service.create_item(db_session, data)
    
    assert item is None
    assert error == "container_not_found"


# Update item tests ---------------------------------------------------------------

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
    result, error = items_service.get_items_paginated(db_session, page=1, page_size=25)
    assert error is None
    assert_pagination_service_response(result, 30, 1, 25, 25)

def test_get_items_paginated_returns_second_page(db_session, room):
    create_items(db_session, None, room.id, quantity=1, count=30)
    result, error = items_service.get_items_paginated(db_session, page=2, page_size=25)
    assert error is None
    assert_pagination_service_response(result, 30, 2, 25, 5)

def test_get_items_paginated_empty_page(db_session, room):
    create_items(db_session, None, room.id, quantity=1, count=10)
    result, error = items_service.get_items_paginated(db_session, page=2, page_size=25)
    assert error is None
    assert_pagination_service_response(result, 10, 2, 25, 0)

def test_get_items_paginated_no_items(db_session):
    result, error = items_service.get_items_paginated(db_session, page=1, page_size=25)
    assert error is None
    assert_pagination_service_response(result, 0, 1, 25, 0)

# Nested relationship tests -------------------------------------------------------

def test_get_items_paginated_includes_room(db_session, room):
    """Items should include nested room with id and name"""
    create_items(db_session, None, room.id, quantity=1, count=1)
    result, error = items_service.get_items_paginated(db_session, page=1, page_size=25)
    
    assert error is None
    assert len(result.data) == 1
    item = result.data[0]
    assert item.room is not None
    assert item.room.id == room.id
    assert item.room.name == room.name

def test_get_items_paginated_includes_container_when_present(db_session, room, container):
    """Items in a container should include nested container with id and name"""
    create_items(db_session, container.id, room.id, quantity=1, count=1)
    result, error = items_service.get_items_paginated(db_session, page=1, page_size=25)
    
    assert error is None
    assert len(result.data) == 1
    item = result.data[0]
    assert item.container is not None
    assert item.container.id == container.id
    assert item.container.name == container.name

def test_get_items_paginated_container_is_none_when_not_in_container(db_session, room):
    """Items not in a container should have container as None"""
    create_items(db_session, None, room.id, quantity=1, count=1)
    result, error = items_service.get_items_paginated(db_session, page=1, page_size=25)
    
    assert error is None
    assert len(result.data) == 1
    item = result.data[0]
    assert item.container is None


# Filter tests -------------------------------------------------------------------

def test_filter_by_name_returns_matching_items(db_session, room):
    """Filter by name returns items with matching name (case-insensitive)"""
    from app.models import Item
    db_session.add_all([
        Item(name="Screwdriver", room_id=room.id, quantity=1),
        Item(name="Hammer", room_id=room.id, quantity=1),
        Item(name="Phillips Screwdriver", room_id=room.id, quantity=1),
    ])
    db_session.commit()
    
    result, error = items_service.get_items_paginated(db_session, name="screwdriver")
    
    assert error is None
    assert result.total == 2
    names = [item.name for item in result.data]
    assert "Screwdriver" in names
    assert "Phillips Screwdriver" in names


def test_filter_by_rooms_returns_items_in_rooms(db_session, floor):
    """Filter by rooms returns only items in specified rooms"""
    from app.models import Room, Item
    room1 = Room(name="Kitchen", floor_id=floor.id)
    room2 = Room(name="Garage", floor_id=floor.id)
    room3 = Room(name="Bedroom", floor_id=floor.id)
    db_session.add_all([room1, room2, room3])
    db_session.commit()
    
    db_session.add_all([
        Item(name="Spatula", room_id=room1.id, quantity=1),
        Item(name="Wrench", room_id=room2.id, quantity=1),
        Item(name="Pillow", room_id=room3.id, quantity=1),
    ])
    db_session.commit()
    
    result, error = items_service.get_items_paginated(db_session, rooms=[room1.id, room2.id])
    
    assert error is None
    assert result.total == 2
    names = [item.name for item in result.data]
    assert "Spatula" in names
    assert "Wrench" in names
    assert "Pillow" not in names


def test_filter_by_containers_returns_items_in_containers(db_session, room):
    """Filter by containers returns only items in specified containers"""
    from app.models import Container, Item
    container1 = Container(name="Toolbox", room_id=room.id)
    container2 = Container(name="Drawer", room_id=room.id)
    db_session.add_all([container1, container2])
    db_session.commit()
    
    db_session.add_all([
        Item(name="Hammer", room_id=room.id, container_id=container1.id, quantity=1),
        Item(name="Scissors", room_id=room.id, container_id=container2.id, quantity=1),
        Item(name="Loose Item", room_id=room.id, container_id=None, quantity=1),
    ])
    db_session.commit()
    
    result, error = items_service.get_items_paginated(db_session, containers=[container1.id])
    
    assert error is None
    assert result.total == 1
    assert result.data[0].name == "Hammer"


def test_filter_by_name_and_rooms(db_session, floor):
    """Filter by name and rooms returns matching items in specified rooms"""
    from app.models import Room, Item
    room1 = Room(name="Kitchen", floor_id=floor.id)
    room2 = Room(name="Garage", floor_id=floor.id)
    db_session.add_all([room1, room2])
    db_session.commit()
    
    db_session.add_all([
        Item(name="Red Screwdriver", room_id=room1.id, quantity=1),
        Item(name="Blue Screwdriver", room_id=room2.id, quantity=1),
        Item(name="Hammer", room_id=room1.id, quantity=1),
    ])
    db_session.commit()
    
    result, error = items_service.get_items_paginated(db_session, name="screwdriver", rooms=[room1.id])
    
    assert error is None
    assert result.total == 1
    assert result.data[0].name == "Red Screwdriver"


def test_filter_by_name_and_containers(db_session, room):
    """Filter by name and containers returns matching items in specified containers"""
    from app.models import Container, Item
    container1 = Container(name="Toolbox", room_id=room.id)
    container2 = Container(name="Drawer", room_id=room.id)
    db_session.add_all([container1, container2])
    db_session.commit()
    
    db_session.add_all([
        Item(name="Red Screwdriver", room_id=room.id, container_id=container1.id, quantity=1),
        Item(name="Blue Screwdriver", room_id=room.id, container_id=container2.id, quantity=1),
        Item(name="Hammer", room_id=room.id, container_id=container1.id, quantity=1),
    ])
    db_session.commit()
    
    result, error = items_service.get_items_paginated(db_session, name="screwdriver", containers=[container1.id])
    
    assert error is None
    assert result.total == 1
    assert result.data[0].name == "Red Screwdriver"


def test_filter_by_rooms_and_containers_valid(db_session, floor):
    """Filter by rooms and containers works when containers belong to rooms"""
    from app.models import Room, Container, Item
    room1 = Room(name="Kitchen", floor_id=floor.id)
    db_session.add(room1)
    db_session.commit()
    
    container1 = Container(name="Toolbox", room_id=room1.id)
    db_session.add(container1)
    db_session.commit()
    
    db_session.add_all([
        Item(name="Hammer", room_id=room1.id, container_id=container1.id, quantity=1),
        Item(name="Loose Item", room_id=room1.id, container_id=None, quantity=1),
    ])
    db_session.commit()
    
    result, error = items_service.get_items_paginated(db_session, rooms=[room1.id], containers=[container1.id])
    
    assert error is None
    assert result.total == 1
    assert result.data[0].name == "Hammer"


def test_filter_by_rooms_and_containers_invalid_returns_error(db_session, floor):
    """Filter by rooms and containers returns error when container not in room"""
    from app.models import Room, Container
    room1 = Room(name="Kitchen", floor_id=floor.id)
    room2 = Room(name="Garage", floor_id=floor.id)
    db_session.add_all([room1, room2])
    db_session.commit()
    
    # Container is in room2, but we'll filter by room1
    container_in_room2 = Container(name="Toolbox", room_id=room2.id)
    db_session.add(container_in_room2)
    db_session.commit()
    
    result, error = items_service.get_items_paginated(db_session, rooms=[room1.id], containers=[container_in_room2.id])
    
    assert result is None
    assert error == "container_room_mismatch"


def test_filter_with_pagination(db_session, room):
    """Filters work correctly with pagination"""
    from app.models import Item
    # Create 30 items with "Widget" in the name
    for i in range(30):
        db_session.add(Item(name=f"Widget {i}", room_id=room.id, quantity=1))
    # Create 5 items without "Widget"
    for i in range(5):
        db_session.add(Item(name=f"Gadget {i}", room_id=room.id, quantity=1))
    db_session.commit()
    
    # First page of filtered results
    result, error = items_service.get_items_paginated(db_session, page=1, page_size=25, name="widget")
    assert error is None
    assert result.total == 30
    assert len(result.data) == 25
    
    # Second page of filtered results
    result, error = items_service.get_items_paginated(db_session, page=2, page_size=25, name="widget")
    assert error is None
    assert result.total == 30
    assert len(result.data) == 5


def test_filter_no_matches_returns_empty(db_session, room):
    """Filter that matches nothing returns empty results"""
    create_items(db_session, None, room.id, quantity=1, count=5)
    
    result, error = items_service.get_items_paginated(db_session, name="nonexistent")
    
    assert error is None
    assert result.total == 0
    assert len(result.data) == 0