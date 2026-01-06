from datetime import datetime, timezone

from pydantic import BaseModel

from .items import ItemResponse, PaginatedItemResponse, ItemCreate


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


class RoomItemCreate(ItemCreate):
    """Proxy schema for creating items within a room context."""


class RoomItemsResponse(PaginatedItemResponse):
    """Proxy schema for paginated items within a room context."""
