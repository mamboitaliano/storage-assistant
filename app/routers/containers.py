from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import qrcode
import os

from ..database import get_db, DATA_DIR
from ..models import Container

router = APIRouter()

# qr codes dir
QR_DIR = os.path.join(DATA_DIR, "qr_codes")
os.makedirs(QR_DIR, exist_ok=True)

class ContainerCreate(BaseModel):
    name: Optional[str] = None


class ContainerResponse(BaseModel):
    id: int
    name: Optional[str]
    qr_code_path: Optional[str]
    item_count: int

    class Config:
        from_attributes = True


@router.post("/", response_model=ContainerResponse)
def create_container(data: ContainerCreate, db: Session = Depends(get_db)): # create a new container
    """Create a new container and generate its QR code"""
    container = Container(name=data.name)
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
            qr_code_path=c.qr_code_path,
            item_count=len(c.items)
        )
        for c in containers
    ]


@router.get("/{container_id}", response_model=ContainerResponse) # ???
def get_container(container_id: int, db: Session = Depends(get_db)):
    """Get a container with all its items and photos"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    return ContainerResponse(
        # todo - why not return container response?
    )


@router.put("/{container_id}")
def update_container(container_id: int, data: ContainerCreate, db: Session = Depends(get_db)):
    """Update a container name"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    container.name = data.name
    db.commit()
    return {"message": "Container updated", "id": container.id}


@router.delete("/{container_id}")
def delete_container(container_id: int, db: Session = Depends(get_db)):
    """Delete a container and all content"""
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # delete QR code if it exists
    if container.qr_code_path:
        qr_file = os.path.join(QR_DIR, container.qr_code_path.lstrip("/static"))
        if os.path.exists(qr_file):
            os.remove(qr_file)

    db.delete(container)
    db.commit()
    return {"message": "Container deleted", "id": container.id}