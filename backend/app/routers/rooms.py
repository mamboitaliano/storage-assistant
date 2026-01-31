from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.rooms import RoomCreate, RoomResponse, RoomItemCreate, PaginatedRoomResponse, RoomOption
from ..schemas.containers import ContainerOption
from ..schemas.items import ItemResponse, PaginatedItemResponse
from ..services import rooms as rooms_service

router = APIRouter()

@router.get("/search", response_model=list[RoomOption])
def search_rooms(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Search rooms by name"""
    rooms = rooms_service.search_rooms(db, q)
    return [RoomOption.model_validate(r) for r in rooms]

@router.post("/", response_model=RoomResponse)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    """Create a new room"""
    return rooms_service.create_room(db, data)

@router.get("/", response_model=PaginatedRoomResponse)
def list_rooms(page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    """List all rooms paginated"""
    return rooms_service.get_rooms_paginated(db, page=page)

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Get a room by ID"""
    room = rooms_service.get_room_detail(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return room

@router.get("/{room_id}/containers", response_model=list[ContainerOption])
def get_room_containers(room_id: int, db: Session = Depends(get_db)):
    """Get all containers for a room"""
    if not rooms_service.get_room(db, room_id):
        raise HTTPException(status_code=404, detail="Room not found")

    return rooms_service.get_containers_for_room(db, room_id)

@router.post("/{room_id}/items", response_model=ItemResponse)
def create_item(room_id: int, data: RoomItemCreate, db: Session = Depends(get_db)):
    """Create a new item in a room, or increment the quantity of an existing item"""
    item = rooms_service.create_item_in_room(db, room_id, data)

    if not item:
        raise HTTPException(status_code=404, detail="Room not found")
    return item

@router.get("/{room_id}/items", response_model=PaginatedItemResponse)
def list_items(
    room_id: int,
    page: int = 1,
    page_size: int = 50,
    db: Session = Depends(get_db)
):
    """List all items in a room (paginated)"""
    items = rooms_service.list_items_in_room(db, room_id, page=page, page_size=page_size)

    if not items:
        raise HTTPException(status_code=404, detail="Room not found")

    return items
