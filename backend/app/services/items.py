from sqlalchemy.orm import Session, joinedload

from ..models import Item, Room, Container
from ..schemas.items import ItemCreate, ItemUpdate, ItemResponse, PaginatedItemResponse

PAGE_SIZE = 25

def create_item(db: Session, data: ItemCreate) -> tuple[ItemResponse | None, str | None]:
    """
    Create a new item.
    
    Returns:
        tuple: (ItemResponse, None) on success
               (None, "room_not_found") if room doesn't exist
               (None, "container_not_found") if container doesn't exist
    """
    # Validate room exists
    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room:
        return None, "room_not_found"
    
    # Validate container exists if provided
    if data.container_id is not None:
        container = db.query(Container).filter(Container.id == data.container_id).first()
        if not container:
            return None, "container_not_found"
    
    # Create the item
    item = Item(
        name=data.name,
        quantity=data.quantity,
        room_id=data.room_id,
        container_id=data.container_id,
    )
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    # Reload with relationships for response
    item = (
        db.query(Item)
        .options(joinedload(Item.room), joinedload(Item.container))
        .filter(Item.id == item.id)
        .first()
    )
    
    return ItemResponse.model_validate(item), None

def get_items_paginated(
        db: Session,
        page: int = 1,
        page_size: int = PAGE_SIZE,
        name: str | None = None,
        rooms: list[int] | None = None,
        containers: list[int] | None = None
    ) -> tuple[PaginatedItemResponse | None, str | None]:
    """
    Get paginated items with optional filters.
    
    Returns:
        tuple: (PaginatedItemResponse, None) on success
               (None, "container_room_mismatch") if containers don't belong to specified rooms
    """
    # If both rooms and containers are provided, validate containers belong to those rooms
    if rooms and containers:
        valid_containers = (
            db.query(Container.id)
            .filter(Container.id.in_(containers), Container.room_id.in_(rooms))
            .all()
        )
        valid_container_ids = {c.id for c in valid_containers}
        invalid_containers = set(containers) - valid_container_ids
        if invalid_containers:
            return None, "container_room_mismatch"
    
    # Build base query
    query = db.query(Item).options(joinedload(Item.room), joinedload(Item.container))
    
    # Apply filters conditionally
    if name:
        query = query.filter(Item.name.ilike(f"%{name}%"))
    
    if containers:
        # Container filter takes precedence (more specific)
        query = query.filter(Item.container_id.in_(containers))
    elif rooms:
        # Only apply room filter if no container filter
        query = query.filter(Item.room_id.in_(rooms))
    
    # Get total count AFTER filters are applied
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return PaginatedItemResponse(
        total=total,
        page=page,
        pageSize=page_size,
        data=items,
    ), None

def get_item(db: Session, item_id: int) -> ItemResponse | None:
    """Get a single item by ID"""
    item = (
        db.query(Item)
        .options(joinedload(Item.room), joinedload(Item.container))
        .filter(Item.id == item_id)
        .first()
    )
    if not item:
        return None
    return ItemResponse.model_validate(item)


def get_items(db: Session) -> list[Item]:
    items = db.query(Item).all()
    return items

def update_item(db: Session, item_id: int, data: ItemUpdate) -> ItemResponse | None:
    item = (
        db.query(Item)
        .options(joinedload(Item.room), joinedload(Item.container))
        .filter(Item.id == item_id)
        .first()
    )
    if not item:
        return None

    # Use exclude_unset to only update fields that were explicitly provided
    # This allows setting container_id to None (to clear it)
    update_data = data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    
    # Reload with relationships for response
    item = (
        db.query(Item)
        .options(joinedload(Item.room), joinedload(Item.container))
        .filter(Item.id == item_id)
        .first()
    )

    return ItemResponse.model_validate(item)

def delete_item(db: Session, item_id: int, quantity: int | None = None) -> dict | None:
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None

    if quantity and quantity < item.quantity:
        item.quantity -= quantity
        db.commit()
        db.refresh(item)
        return {"message": "Item quantity reduced", "id": item.id, "quantity": item.quantity}

    db.delete(item)
    db.commit()
    return {"message": "Item deleted", "id": item.id}
