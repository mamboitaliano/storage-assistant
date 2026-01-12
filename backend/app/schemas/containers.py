from pydantic import BaseModel, ConfigDict

from .items import ItemResponse, ItemCreate


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


class ContainerDetailResponse(ContainerResponse):
    items: list[ItemResponse]


class ContainerItemCreate(ItemCreate):
    """Proxy schema for creating items within a container context."""
