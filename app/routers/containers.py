from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import qrcode
import os

from ..database import get_db, DATA_DIR
from ..models import Container, Item
from .items import ItemResponse, ItemCreate

router = APIRouter()

# qr codes dir
QR_DIR = os.path.join(DATA_DIR, "qr_codes")
os.makedirs(QR_DIR, exist_ok=True)

class ContainerCreate(BaseModel):
    name: str | None = None
    room_id: int | None = None

class ContainerResponse(BaseModel):
    id: int
    name: str | None = None
    room_id: int | None = None
    qr_code_path: str | None = None
    item_count: int = 0

    class Config:
        from_attributes = True

class ContainerDetailResponse(ContainerResponse):
    items: list[ItemResponse]

@router.post("/", response_model=ContainerResponse)
def create_container(data: ContainerCreate, db: Session = Depends(get_db)): # create a new container
    """Create a new container and generate its QR code"""
    container = Container(name=data.name, room_id=data.room_id)

    db.add(container)
    db.commit()
    db.refresh(container)

    # generate QR code with URL to this container
    qr_filename = f"container_{container.id}.png"
    qr_path = os.path.join(QR_DIR, qr_filename)

    # QR contains relative url that will work on the lan
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
        item_count=0 # no items yet
    )

@router.get("/", response_model=list[ContainerResponse])
def list_containers(db: Session = Depends(get_db)):
    """List all containers"""
    containers = db.query(Container).all()

    return [
        ContainerResponse(
            id=c.id,
            name=c.name,
            room_id=c.room_id,
            qr_code_path=c.qr_code_path,
            item_count=len(c.items)
        )
        for c in containers
    ]

@router.get("/{container_id}", response_model=ContainerDetailResponse)
def get_container(container_id: int, db: Session = Depends(get_db)):
    """Get a container with all its items and photos"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

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
                quantity=item.quantity
            )
            for item in container.items
        ]
    )

@router.put("/{container_id}")
def update_container(container_id: int, data: ContainerCreate, db: Session = Depends(get_db)):
    """Update a container name"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

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
                quantity=item.quantity
            )
            for item in container.items
        ]
    )

@router.delete("/{container_id}")
def delete_container(container_id: int, db: Session = Depends(get_db)):
    """Delete a container and all content"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # delete QR code if it exists
    if container.qr_code_path:
        qr_file = os.path.join(QR_DIR, os.path.basename(container.qr_code_path))
        
        if os.path.exists(qr_file):
            os.remove(qr_file)

    db.delete(container)
    db.commit()
    return {"message": "Container deleted", "id": container.id}

@router.post("/{container_id}/items", response_model=ItemResponse)
def create_item(container_id: int, data: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item in a container, or increment the quantity of an existing item"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # check if an item with the same name already exists in the container
    existing_item = db.query(Item).filter(
        Item.container_id == container_id,
        Item.name.ilike(data.name)
    ).first()

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
            created_at=existing_item.created_at
        )

    # create a new item
    item = Item(name=data.name, container_id=container_id)
    db.add(item)
    db.commit()
    db.refresh(item)

    return ItemResponse(
        id=item.id,
        name=item.name,
        room_id=item.room_id,
        container_id=item.container_id,
        quantity=item.quantity,
        created_at=item.created_at
    )