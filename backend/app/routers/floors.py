from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import floors as floors_service
from ..schemas.floors import FloorCreate, FloorResponse, PaginatedFloorResponse

router = APIRouter()

@router.post("/", response_model=FloorResponse)
def create_floor(data: FloorCreate, db: Session = Depends(get_db)):
    """Create a new floor"""
    return floors_service.create_floor(db, data)

@router.get("/", response_model=PaginatedFloorResponse)
def list_floors(page: int = Query(1, ge=1),db: Session = Depends(get_db)):
    """List all floors"""
    return floors_service.list_floors_paginated(db, page=page)

@router.get("/{floor_id}", response_model=FloorResponse)
def get_floor(floor_id: int, db: Session = Depends(get_db)):
    """Get a floor by ID"""
    floor = floors_service.get_floor_detail(db, floor_id)
    
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")

    return floor

@router.delete("/{floor_id}")
async def delete_floor(floor_id: int, db: Session = Depends(get_db)):
    """Delete a floor by ID"""
    try:
        await floors_service.delete_floor(db, floor_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"message": "Floor deleted successfully"}