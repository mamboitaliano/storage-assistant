from sqlalchemy.orm import Session, joinedload

from ..models import Item
from ..schemas.items import ItemUpdate, ItemResponse, PaginatedItemResponse

PAGE_SIZE = 25

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
