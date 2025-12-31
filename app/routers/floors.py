from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timezone

from ..database import get_db
from ..models import Floor

router = APIRouter()

class FloorCreate(BaseModel):
    name: str | None = None
    floor_number: int | None = None

class FloorResponse(BaseModel):
    id: int
    name: str | None = None
    floor_number: int | None = None
    created_at: datetime = datetime.now(timezone.utc)

    class Config:
        from_attributes = True

@router.post("/", response_model=FloorResponse)
def create_floor(data: FloorCreate, db: Session = Depends(get_db)):
    """Create a new floor"""
    floor = Floor(name=data.name, floor_number=data.floor_number)
    
    db.add(floor)
    db.commit()
    db.refresh(floor)
    return FloorResponse(
        id=floor.id,
        name=floor.name,
        floor_number=floor.floor_number,
        created_at=floor.created_at
    )

@router.get("/", response_model=list[FloorResponse])
def list_floors(db: Session = Depends(get_db)):
    """List all floors"""
    floors = db.query(Floor).all()

    return [
        FloorResponse(
            id=f.id,
            name=f.name,
            floor_number=f.floor_number,
            created_at=f.created_at
        )
        for f in floors
    ]

@router.get("/{floor_id}", response_model=FloorResponse)
def get_floor(floor_id: int, db: Session = Depends(get_db)):
    """Get a floor by ID"""
    floor = db.query(Floor).filter(Floor.id == floor_id).first()
    
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    
    return FloorResponse(
        id=floor.id,
        name=floor.name,
        floor_number=floor.floor_number,
        created_at=floor.created_at
    )