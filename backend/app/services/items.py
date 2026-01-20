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


def get_items_paginated(db: Session, page: int = 1, page_size: int = PAGE_SIZE) -> PaginatedItemResponse:
    """Get paginated items"""
    total = db.query(Item).count()
    offset = (page - 1) * page_size
    items = (
        db.query(Item)
        .options(joinedload(Item.room), joinedload(Item.container))
        .offset(offset)
        .limit(page_size)
        .all()
    )
    
    return PaginatedItemResponse(
        total=total,
        page=page,
        pageSize=page_size,
        data=items,
    )

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

    if data.name is not None:
        item.name = data.name
    if data.room_id is not None:
        item.room_id = data.room_id
    if data.container_id is not None:
        item.container_id = data.container_id
    if data.quantity is not None:
        item.quantity = data.quantity

    db.commit()
    db.refresh(item)

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
