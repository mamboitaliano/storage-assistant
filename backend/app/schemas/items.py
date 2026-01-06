from datetime import datetime, timezone

from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    quantity: int
    room_id: int | None = None
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

    class Config:
        from_attributes = True


class PaginatedItemResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True
