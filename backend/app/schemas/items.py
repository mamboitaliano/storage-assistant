from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict

class ItemRoomResponse(BaseModel):
    id: int
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)

class ItemContainerResponse(BaseModel):
    id: int
    name: str | None = None

    model_config = ConfigDict(from_attributes=True)

class ItemCreateBase(BaseModel):
    """Base schema for item creation - used by nested endpoints"""
    name: str
    quantity: int = 1

class ItemCreate(ItemCreateBase):
    """Schema for POST /items - requires room_id"""
    room_id: int  # Required - room must exist
    container_id: int | None = None

class ItemUpdate(BaseModel):
    name: str | None = None
    quantity: int | None = None
    room_id: int | None = None
    container_id: int | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    room_id: int
    container_id: int | None = None
    quantity: int
    created_at: datetime = datetime.now(timezone.utc)
    room: ItemRoomResponse
    container: ItemContainerResponse | None = None

    model_config = ConfigDict(from_attributes=True)

class PaginatedItemResponse(BaseModel):
    data: list[ItemResponse]
    total: int
    page: int
    pageSize: int

    model_config = ConfigDict(from_attributes=True)
