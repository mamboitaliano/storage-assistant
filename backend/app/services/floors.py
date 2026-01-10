from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import Container, Floor, Item, Room
from ..schemas.floors import FloorCreate, FloorResponse, RoomResponse


def create_floor(db: Session, data: FloorCreate) -> FloorResponse:
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


def list_floors_with_counts(db: Session) -> list[FloorResponse]:
    rows = (
        db.query(Floor, func.count(Room.id).label("room_count"))
        .outerjoin(Room, Floor.id == Room.floor_id)
        .group_by(Floor.id)
        .all()
    )

    return [
        FloorResponse(
            id=f.id,
            name=f.name,
            floor_number=f.floor_number,
            created_at=f.created_at,
            room_count=room_count,
            rooms=None,
        )
        for f, room_count in rows
    ]


def get_floor_detail(db: Session, floor_id: int) -> FloorResponse | None:
    floor = db.query(Floor).filter(Floor.id == floor_id).first()

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
    floor = db.query(Floor).filter(Floor.id == floor_id).first()

    if not floor:
        raise ValueError("Floor not found")

    rooms = db.query(Room).filter(Room.floor_id == floor_id).all()
    # TODO: we'll need to figure out all rooms on the floor and delete them, and all items/containers assigned to these rooms
    # will need to be deleted as well. The frontend should prompt the user to move the items/containers to different rooms first.

    db.delete(floor)
    db.commit()

    return None
