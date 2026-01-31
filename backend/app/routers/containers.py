from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.containers import (
    ContainerCreate,
    ContainerResponse,
    ContainerDetailResponse,
    ContainerItemCreate,
    ContainerOption,
    PaginatedContainerResponse,
)
from ..schemas.items import ItemResponse
from ..services import containers as containers_service

router = APIRouter()

@router.get("/search", response_model=list[ContainerOption])
def search_containers(
    q: str = Query(..., min_length=1),
    rooms: str | None = Query(None),
    db: Session = Depends(get_db)
):
    """Search containers by name, optionally filtered by rooms"""
    room_ids = [int(r) for r in rooms.split(",")] if rooms else None
    containers = containers_service.search_containers(db, q, room_ids)
    return [ContainerOption.model_validate(c) for c in containers]

@router.post("/", response_model=ContainerResponse)
def create_container(data: ContainerCreate, db: Session = Depends(get_db)): # create a new container
    """Create a new container and generate its QR code"""
    return containers_service.create_container(db, data)

@router.get("/", response_model=PaginatedContainerResponse)
def list_containers(page: int = Query(1, ge=1),db: Session = Depends(get_db)):
    """List all containers"""
    return containers_service.list_containers_paginated(db, page=page)

@router.get("/{container_id}", response_model=ContainerDetailResponse)
def get_container(container_id: int, db: Session = Depends(get_db)):
    """Get a container with all its items and photos"""
    container = containers_service.get_container_detail(db, container_id)
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    return container

@router.put("/{container_id}")
def update_container(container_id: int, data: ContainerCreate, db: Session = Depends(get_db)):
    """Update a container name"""
    container = containers_service.update_container(db, container_id, data)
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    return container

@router.delete("/{container_id}")
def delete_container(container_id: int, db: Session = Depends(get_db)):
    """Delete a container and all content"""
    result = containers_service.delete_container(db, container_id)
    if not result:
        raise HTTPException(status_code=404, detail="Container not found")
    return result

@router.post("/{container_id}/items", response_model=ItemResponse)
def create_item(container_id: int, data: ContainerItemCreate, db: Session = Depends(get_db)):
    """Create a new item in a container, or increment the quantity of an existing item"""
    item = containers_service.create_item_in_container(db, container_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Container not found")

    return item
