from pydantic import BaseModel, ConfigDict
from .items import ItemResponse, ItemCreateBase

class ContainerCreate(BaseModel):
    name: str | None = None
    room_id: int | None = None

class ContainerResponse(BaseModel):
    id: int
    name: str | None = None
    room_id: int | None = None
    qr_code_path: str | None = None
    item_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class PaginatedContainerResponse(BaseModel):
    data: list[ContainerResponse]
    total: int
    page: int
    pageSize: int

    model_config = ConfigDict(from_attributes=True)

class ContainerDetailResponse(ContainerResponse):
    items: list[ItemResponse]

class ContainerItemCreate(ItemCreateBase):
    """Schema for creating items within a container context (container_id from URL)."""
