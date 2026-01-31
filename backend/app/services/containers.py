import os

import qrcode
from sqlalchemy.orm import Session, joinedload

from ..database import DATA_DIR
from ..models import Container, Item
from ..schemas.containers import (
    ContainerCreate,
    ContainerResponse,
    ContainerDetailResponse,
    ContainerItemCreate,
    PaginatedContainerResponse,
)
from ..schemas.items import ItemResponse

# QR codes directory
QR_DIR = os.path.join(DATA_DIR, "qr_codes")
os.makedirs(QR_DIR, exist_ok=True)

PAGE_SIZE = 25

def create_container(db: Session, data: ContainerCreate) -> ContainerResponse:
    """Create a new container"""
    container = Container(name=data.name, room_id=data.room_id)

    db.add(container)
    db.commit()
    db.refresh(container)

    qr_filename = f"container_{container.id}.png"
    qr_path = os.path.join(QR_DIR, qr_filename)

    qr_url = f"/containers/{container.id}"
    qr = qrcode.make(qr_url)
    qr.save(qr_path)

    container.qr_code_path = f"/static/qr_codes/{qr_filename}"
    db.commit()
    db.refresh(container)

    return ContainerResponse(
        id=container.id,
        name=container.name,
        room_id=container.room_id,
        qr_code_path=container.qr_code_path,
        item_count=0,
    )

def list_containers_paginated(db: Session, page: int = 1, page_size: int = PAGE_SIZE) -> PaginatedContainerResponse:
    """List containers with pagination"""
    total = db.query(Container).count()
    offset = (page - 1) * page_size
    containers = db.query(Container).offset(offset).limit(page_size).all()

    return PaginatedContainerResponse(
        data=[
            ContainerResponse(
                id=c.id,
                name=c.name,
                room_id=c.room_id,
                qr_code_path=c.qr_code_path,
                item_count=len(c.items),
            )
            for c in containers
        ],
        total=total,
        page=page,
        pageSize=page_size,
    )

def get_container_detail(db: Session, container_id: int) -> ContainerDetailResponse | None:
    """Get a container with all its details"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        return None

    return ContainerDetailResponse(
        id=container.id,
        name=container.name,
        room_id=container.room_id,
        qr_code_path=container.qr_code_path,
        item_count=len(container.items),
        items=[
            ItemResponse(
                id=item.id,
                name=item.name,
                room_id=item.room_id,
                container_id=item.container_id,
                quantity=item.quantity,
                created_at=item.created_at,
            )
            for item in container.items
        ],
    )

def update_container(db: Session, container_id: int, data: ContainerCreate) -> ContainerDetailResponse | None:
    """Update a container"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        return None

    container.name = data.name
    container.room_id = data.room_id
    db.commit()
    db.refresh(container)

    return ContainerDetailResponse(
        id=container.id,
        name=container.name,
        room_id=container.room_id,
        qr_code_path=container.qr_code_path,
        item_count=len(container.items),
        items=[
            ItemResponse(
                id=item.id,
                name=item.name,
                room_id=item.room_id,
                container_id=item.container_id,
                quantity=item.quantity,
                created_at=item.created_at,
            )
            for item in container.items
        ],
    )

def delete_container(db: Session, container_id: int) -> dict | None:
    """Delete a container"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        return None

    if container.qr_code_path:
        qr_file = os.path.join(QR_DIR, os.path.basename(container.qr_code_path))

        if os.path.exists(qr_file):
            os.remove(qr_file)

    db.delete(container)
    db.commit()
    return {"message": "Container deleted", "id": container.id}

def search_containers(db: Session, query: str, room_ids: list[int] | None = None) -> list[Container]:
    """Search containers by name (case-insensitive), optionally filtered by rooms"""
    q = db.query(Container).filter(Container.name.ilike(f"%{query}%"))
    
    if room_ids:
        q = q.filter(Container.room_id.in_(room_ids))
    
    return q.limit(50).all()


def create_item_in_container(db: Session, container_id: int, data: ContainerItemCreate) -> ItemResponse | None:
    """Create a new item in a container"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        return None

    existing_item = (
        db.query(Item)
        .options(joinedload(Item.room), joinedload(Item.container))
        .filter(
            Item.container_id == container_id,
            Item.name.ilike(data.name),
        )
        .first()
    )

    if existing_item:
        existing_item.quantity += data.quantity
        db.commit()
        db.refresh(existing_item)

        return ItemResponse.model_validate(existing_item)

    item = Item(
        name=data.name,
        container_id=container_id,
        room_id=container.room_id,
        quantity=data.quantity,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return ItemResponse.model_validate(item)
