from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timezone

from ..database import get_db
from ..models import Item

router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    quantity: int
    room_id: int | None = None
    container_id: int | None = None

class ItemUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None
    room_id: int | None = None
    container_id: int | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    room_id: int
    container_id: int | None = None
    quantity: int
    created_at: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True

class PaginatedItemResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True

@router.put("/{item_id}")
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    """Update an item's name or quantity"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if data.name is not None:
        item.name = data.name
    if data.room_id is not None:
        item.room_id = data.room_id
    if data.container_id is not None:
        item.container_id = data.container_id
    if data.quantity is not None:
        item.quantity = data.quantity

    db.commit()
    return ItemResponse(
        id=item.id,
        name=item.name,
        room_id=item.room_id,
        container_id=item.container_id,
        quantity=item.quantity,
        created_at=item.created_at
    )


@router.delete("/{item_id}")
def delete_item(item_id: int, quantity: int = None, db: Session = Depends(get_db)):
    """
    Delete an item or reduce its quantity.
    If quantity is provided and less than current, reduces quantity.
    Otherwise deletes the item.
    """
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if quantity and quantity < item.quantity:
        item.quantity -= quantity
        db.commit()
        return {"message": "Item quantity reduced", "id": item.id, "quantity": item.quantity}
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted", "id": item.id}