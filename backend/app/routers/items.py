from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.items import ItemCreate, ItemUpdate, ItemResponse
from ..services import items as items_service

router = APIRouter()

@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item assigned to a room and optionally a container."""
    item, error = items_service.create_item(db, data=data)
    
    if error == "room_not_found":
        raise HTTPException(status_code=404, detail="Room not found")
    if error == "container_not_found":
        raise HTTPException(status_code=404, detail="Container not found")
    
    return item

@router.get("/")
def get_items(
        page: int = Query(1, ge=1),
        name: str | None = Query(None),
        rooms: str | None = Query(None),
        containers: str | None = Query(None),
        db: Session = Depends(get_db)
    ):
    """Get all items with optional filters"""
    room_ids = [int(r) for r in rooms.split(",")] if rooms else None
    container_ids = [int(c) for c in containers.split(",")] if containers else None
    
    result, error = items_service.get_items_paginated(
        db, page=page, name=name, rooms=room_ids, containers=container_ids
    )
    
    if error == "container_room_mismatch":
        raise HTTPException(
            status_code=400,
            detail="One or more containers do not belong to the specified rooms"
        )
    
    return result

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
