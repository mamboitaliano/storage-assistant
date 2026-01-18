from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)


class PaginatedItemResponse(BaseModel):
    data: list[ItemResponse]
    total: int
    page: int
    pageSize: int

    model_config = ConfigDict(from_attributes=True)
