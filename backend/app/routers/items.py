from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.items import ItemUpdate, ItemResponse
from ..services import items as items_service

router = APIRouter()

@router.get("/")
def get_items(db: Session = Depends(get_db)):
    """Get all items"""
    items = items_service.get_items(db)
    return items

@router.put("/{item_id}")
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    """Update an item's name or quantity"""
    item = items_service.update_item(db, item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.delete("/{item_id}")
def delete_item(item_id: int, quantity: int = None, db: Session = Depends(get_db)):
    """
    Delete an item or reduce its quantity.
    If quantity is provided and less than current, reduces quantity.
    Otherwise deletes the item.
    """
    result = items_service.delete_item(db, item_id, quantity)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    return result
