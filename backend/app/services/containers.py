import os

import qrcode
from sqlalchemy.orm import Session

from ..database import DATA_DIR
from ..models import Container, Item
from ..schemas.containers import (
    ContainerCreate,
    ContainerResponse,
    ContainerDetailResponse,
    ContainerItemCreate,
)
from ..schemas.items import ItemResponse

# QR codes directory
QR_DIR = os.path.join(DATA_DIR, "qr_codes")
os.makedirs(QR_DIR, exist_ok=True)


def create_container(db: Session, data: ContainerCreate) -> ContainerResponse:
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


def list_containers(db: Session) -> list[ContainerResponse]:
    containers = db.query(Container).all()

    return [
        ContainerResponse(
            id=c.id,
            name=c.name,
            room_id=c.room_id,
            qr_code_path=c.qr_code_path,
            item_count=len(c.items),
        )
        for c in containers
    ]


def get_container_detail(db: Session, container_id: int) -> ContainerDetailResponse | None:
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


def create_item_in_container(db: Session, container_id: int, data: ContainerItemCreate) -> ItemResponse | None:
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        return None

    existing_item = (
        db.query(Item)
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

        return ItemResponse(
            id=existing_item.id,
            name=existing_item.name,
            room_id=existing_item.room_id,
            container_id=existing_item.container_id,
            quantity=existing_item.quantity,
            created_at=existing_item.created_at,
        )

    item = Item(
        name=data.name,
        container_id=container_id,
        room_id=container.room_id,
        quantity=data.quantity,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return ItemResponse(
        id=item.id,
        name=item.name,
        room_id=item.room_id,
        container_id=item.container_id,
        quantity=item.quantity,
        created_at=item.created_at,
    )
