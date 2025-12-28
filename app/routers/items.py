from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db
from ..models import Container, Item

router = APIRouter()

class ItemCreate(BaseModel):
    container_id: int
    name: str
    quantity: int = 1

class ItemUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None


@router.post("/")
def add_item(data: ItemCreate, db: Session = Depends(get_db)):
    """Add an item to a container"""
    container = db.query(Container).filter(Container.id == data.container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    
    # check if an item with this name already exists in this container
    existing = db.query(Item).filter(Item.container_id == data.container_id, Item.name.ilike(data.name)).first()

    if existing:
        existing.quantity += data.quantity
        db.commit()
        return {"message": "{data.name} quantity updated", "id": existing.id, "quantity": existing.quantity}
    
    item = Item(
        container_id=data.container_id,
        name=data.name,
        quantity=data.quantity
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {"message": "{data.name} added to container", "id": item.id, "quantity": item.quantity}


@router.put("/{item_id}")
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    """Update an item's name or quantity"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if data.name is not None:
        item.name = data.name
    if data.quantity is not None:
        item.quantity = data.quantity

    db.commit()
    return {"message": "Item updated", "id": item.id, "quantity": item.quantity}


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