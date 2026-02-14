from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict

from .items import PaginatedItemResponse, ItemCreateBase

class RoomCreate(BaseModel):
    name: str | None = None
    floor_id: int | None = None

class RoomUpdate(BaseModel):
    name: str | None = None
    floor_id: int | None = None

class RoomResponse(BaseModel):
    id: int
    name: str | None = None
    floor_id: int | None = None
    created_at: datetime = datetime.now(timezone.utc)
    container_count: int | None = None
    item_count: int | None = None

    model_config = ConfigDict(from_attributes=True)

class PaginatedRoomResponse(BaseModel):
    data: list[RoomResponse]
    total: int
    page: int
    pageSize: int

    model_config = ConfigDict(from_attributes=True)

class RoomOption(BaseModel):
    """Lightweight room for dropdowns"""
    id: int
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)

class RoomOptionsResponse(BaseModel):
    """Response for listing all rooms (with limit)"""
    data: list[RoomOption]
    total: int
    hasMore: bool

    model_config = ConfigDict(from_attributes=True)

class RoomItemCreate(ItemCreateBase):
    """Schema for creating items within a room context (room_id from URL)."""

class RoomItemsResponse(PaginatedItemResponse):
    """Proxy schema for paginated items within a room context."""
