from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Container, Floor, Item, Room
from ..schemas.floors import FloorCreate, FloorResponse, RoomResponse, PaginatedFloorResponse
from ..schemas.rooms import RoomOption

PAGE_SIZE = 25

def create_floor(db: Session, data: FloorCreate) -> FloorResponse:
    """Create a new floor"""
    floor = Floor(name=data.name, floor_number=data.floor_number)

    db.add(floor)
    db.commit()
    db.refresh(floor)

    return FloorResponse(
        id=floor.id,
        name=floor.name,
        floor_number=floor.floor_number,
        created_at=floor.created_at,
        room_count=0,
        rooms=None,
    )

def list_floors_paginated(db: Session, page: int = 1, page_size: int = PAGE_SIZE) -> PaginatedFloorResponse:
    """List floors with pagination and room counts"""
    total = db.query(Floor).count()
    offset = (page - 1) * page_size

    rows = (
        db.query(Floor, func.count(Room.id).label("room_count"))
        .outerjoin(Room, Floor.id == Room.floor_id)
        .group_by(Floor.id)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return PaginatedFloorResponse(
        data=[
            FloorResponse(
                id=f.id,
                name=f.name,
                floor_number=f.floor_number,
                created_at=f.created_at,
                room_count=room_count,
                rooms=None,
            )
            for f, room_count in rows
        ],
        total=total,
        page=page,
        pageSize=page_size,
    )

def get_rooms_for_floor(db: Session, floor_id: int) -> list[RoomOption]:
    rooms = db.query(Room).filter(Room.floor_id == floor_id).all()
    return [RoomOption.model_validate(r) for r in rooms]

def get_floor_detail(db: Session, floor_id: int) -> FloorResponse | None:
    """Get a floor by ID"""
    floor = get_floor(db, floor_id)

    if not floor:
        return None

    rooms_with_counts = (
        db.query(
            Room,
            func.count(func.distinct(Item.id)).label("item_count"),
            func.count(func.distinct(Container.id)).label("container_count"),
        )
        .outerjoin(Item, Item.room_id == Room.id)
        .outerjoin(Container, Container.room_id == Room.id)
        .filter(Room.floor_id == floor_id)
        .group_by(Room.id)
        .all()
    )

    return FloorResponse(
        id=floor.id,
        name=floor.name,
        floor_number=floor.floor_number,
        created_at=floor.created_at,
        room_count=len(rooms_with_counts),
        rooms=[
            RoomResponse(
                id=room.id,
                name=room.name,
                floor_id=room.floor_id,
                created_at=room.created_at,
                item_count=item_count,
                container_count=container_count,
            )
            for room, item_count, container_count in rooms_with_counts
        ],
    )

def delete_floor(db: Session, floor_id: int) -> None:
    """Delete a floor"""
    floor = get_floor(db, floor_id)

    if not floor:
        raise ValueError("Floor not found")

    rooms = db.query(Room).filter(Room.floor_id == floor_id).all()
    # TODO: we'll need to figure out all rooms on the floor and delete them, and all items/containers assigned to these rooms
    # will need to be deleted as well. The frontend should prompt the user to move the items/containers to different rooms first.

    db.delete(floor)
    db.commit()

    return None

def get_floor(db: Session, floor_id: int) -> Floor | None:
    return db.query(Floor).filter(Floor.id == floor_id).first()
