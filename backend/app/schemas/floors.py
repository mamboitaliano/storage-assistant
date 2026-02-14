from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict
from .rooms import RoomResponse

class FloorCreate(BaseModel):
    name: str | None = None
    floor_number: int | None = None

class FloorUpdate(BaseModel):
    name: str | None = None
    floor_number: int | None = None

class FloorResponse(BaseModel):
    id: int
    name: str | None = None
    floor_number: int | None = None
    created_at: datetime = datetime.now(timezone.utc)
    room_count: int = 0
    rooms: list[RoomResponse] | None = None

    model_config = ConfigDict(from_attributes=True)

class PaginatedFloorResponse(BaseModel):
    data: list[FloorResponse]
    total: int
    page: int
    pageSize: int

    model_config = ConfigDict(from_attributes=True)