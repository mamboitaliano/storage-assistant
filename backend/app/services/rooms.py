from math import ceil
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..models import Room, Item, Container
from ..schemas.rooms import RoomCreate, RoomResponse, RoomItemsResponse, RoomItemCreate, PaginatedRoomResponse
from ..schemas.items import ItemResponse

PAGE_SIZE = 25

def create_room(db: Session, data: RoomCreate) -> RoomResponse:
    room = Room(name=data.name, floor_id=data.floor_id)

    db.add(room)
    db.commit()
    db.refresh(room)

    return RoomResponse(
        id=room.id,
        name=room.name,
        floor_id=room.floor_id,
        created_at=room.created_at,
    )

def get_rooms_paginated(db: Session, page: int = 1, page_size: int = PAGE_SIZE) -> PaginatedRoomResponse:
    """List rooms with pagination"""
    total = db.query(Room).count()
    offset = (page - 1) * page_size
    rooms = (
        db.query(
            Room,
            func.count(func.distinct(Container.id)).label("container_count"),
            func.count(func.distinct(Item.id)).label("item_count"),
        )
        .outerjoin(Container, Room.id == Container.room_id)
        .outerjoin(Item, Room.id == Item.room_id)
        .group_by(Room.id)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return PaginatedRoomResponse(
        data=[
            RoomResponse(
                id=r.Room.id,
                name=r.Room.name,
                floor_id=r.Room.floor_id,
                created_at=r.Room.created_at,
                container_count=r.container_count,
                item_count=r.item_count,
            )
            for r in rooms
        ],
        total=total,
        page=page,
        pageSize=page_size,
    )

def get_room(db: Session, room_id: int) -> RoomResponse | None:
    result = (
        db.query(
            Room,
            func.count(func.distinct(Container.id)).label('container_count'),
            func.count(func.distinct(Item.id)).label('item_count'),
        )
        .outerjoin(Container, Room.id == Container.room_id)
        .outerjoin(Item, Room.id == Item.room_id)
        .filter(Room.id == room_id)
        .group_by(Room.id)
        .first()
    )

    if not result:
        return None

    return RoomResponse(
        id=result.Room.id,
        name=result.Room.name,
        floor_id=result.Room.floor_id,
        created_at=result.Room.created_at,
        container_count=result.container_count,
        item_count=result.item_count,
    )

def create_item_in_room(db: Session, room_id: int, data: RoomItemCreate) -> ItemResponse | None:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None

    existing_item = (
        db.query(Item)
        .options(joinedload(Item.room), joinedload(Item.container))
        .filter(
            Item.room_id == room_id,
            Item.container_id == None,
            Item.name.ilike(data.name),
        )
        .first()
    )

    if existing_item:
        existing_item.quantity += data.quantity
        db.commit()
        db.refresh(existing_item)
        return ItemResponse.model_validate(existing_item)

    item = Item(
        name=data.name,
        room_id=room_id,
        quantity=data.quantity,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return ItemResponse.model_validate(item)

def list_items_in_room(
    db: Session,
    room_id: int,
    page: int = 1,
    page_size: int = 50,
) -> RoomItemsResponse | None:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None

    page_size = min(page_size, 100)
    skip = (page - 1) * page_size

    total = db.query(Item).filter(Item.room_id == room_id).count()
    total_pages = ceil(total / page_size) if total > 0 else 1

    items = (
        db.query(Item)
        .options(joinedload(Item.room), joinedload(Item.container))
        .filter(Item.room_id == room_id)
        .offset(skip)
        .limit(page_size)
        .all()
    )

    return RoomItemsResponse(
        items=[
            ItemResponse(
                id=i.id,
                name=i.name,
                room_id=i.room_id,
                container_id=i.container_id,
                quantity=i.quantity,
                created_at=i.created_at,
            )
            for i in items
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
