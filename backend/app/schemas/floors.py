from datetime import datetime, timezone

from pydantic import BaseModel


class FloorCreate(BaseModel):
    name: str | None = None
    floor_number: int | None = None


class RoomResponse(BaseModel):
    id: int
    name: str | None = None
    floor_id: int | None = None
    created_at: datetime = datetime.now(timezone.utc)
    item_count: int = 0
    container_count: int = 0

    class Config:
        from_attributes = True


class FloorResponse(BaseModel):
    id: int
    name: str | None = None
    floor_number: int | None = None
    created_at: datetime = datetime.now(timezone.utc)
    room_count: int = 0
    rooms: list[RoomResponse] | None = None

    class Config:
        from_attributes = True
