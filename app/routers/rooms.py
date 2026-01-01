from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timezone
from math import ceil

from ..database import get_db
from ..models import Room, Floor, Item
from .items import ItemResponse, ItemCreate, PaginatedItemResponse

router = APIRouter()

class RoomCreate(BaseModel):
    name: str | None = None
    floor_id: int | None = None

class RoomResponse(BaseModel):
    id: int
    name: str | None = None
    floor_id: int | None = None
    created_at: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True

@router.post("/", response_model=RoomResponse)
def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    """Create a new room"""
    room = Room(name=data.name, floor_id=data.floor_id)

    db.add(room)
    db.commit()
    db.refresh(room)
    
    return RoomResponse(
        id=room.id,
        name=room.name,
        floor_id=room.floor_id,
        created_at=room.created_at
    )

@router.get("/", response_model=list[RoomResponse])
def list_rooms(db: Session = Depends(get_db)):
    """List all rooms"""
    rooms = db.query(Room).all()

    return [
        RoomResponse(
            id=r.id,
            name=r.name,
            floor_id=r.floor_id,
            created_at=r.created_at
        )
        for r in rooms
    ]

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """Get a room by ID"""
    room = db.query(Room).filter(Room.id == room_id).first()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return RoomResponse(
        id=room.id,
        name=room.name,
        floor_id=room.floor_id,
        created_at=room.created_at
    )

@router.post("/{room_id}/items", response_model=ItemResponse)
def create_item(room_id: int, data: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item in a room, or increment the quantity of an existing item"""
    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # check if an item with the same name already exists in the room
    existing_item = db.query(Item).filter(
        Item.room_id == room_id,
        Item.container_id == None,
        Item.name.ilike(data.name)
    ).first()

    if existing_item:
        existing_item.quantity += data.quantity
        db.commit()
        db.refresh(existing_item)

        return ItemResponse(
            id=existing_item.id,
            name=existing_item.name,
            room_id=existing_item.room_id,
            quantity=existing_item.quantity,
            created_at=existing_item.created_at
        )

    # create a new item
    item = Item(
        name=data.name,
        room_id=room_id,
        quantity=data.quantity
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return ItemResponse(
        id=item.id,
        name=item.name,
        room_id=item.room_id,
        quantity=item.quantity,
        created_at=item.created_at
    )

@router.get("/{room_id}/items", response_model=PaginatedItemResponse)
def list_items(
    room_id: int,
    page: int = 1,
    page_size: int = 50,
    db: Session = Depends(get_db)
):
    """List all items in a room (paginated)"""
    room = db.query(Room).filter(Room.id == room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Cap page size to 100
    page_size = min(page_size, 100)

    # Calculate skip from page
    skip = (page - 1) * page_size

    # Get total count of items
    total = db.query(Item).filter(Item.room_id == room_id).count()
    total_pages = ceil(total / page_size) if total > 0 else 1

    # Get the paginated items
    items = db.query(Item).filter(
        Item.room_id == room_id
    ).offset(skip).limit(page_size).all()

    return PaginatedItemResponse(
        items=[
            ItemResponse(
                id=i.id,
                name=i.name,
                room_id=i.room_id,
                container_id=i.container_id,
                quantity=i.quantity,
                created_at=i.created_at
            )
            for i in items
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


