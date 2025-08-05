from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from . import schemas, crud

router = APIRouter()

@router.post("/", response_model=schemas.Specialty, status_code=status.HTTP_201_CREATED)
def create_specialty(specialty: schemas.SpecialtyCreate, db: Session = Depends(get_db)):
    db_specialty = crud.get_specialty_by_name(db, name=specialty.name)
    if db_specialty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Specialty with this name already exists",
        )
    return crud.create_specialty(db=db, specialty=specialty)

@router.get("/", response_model=List[schemas.Specialty])
def read_specialties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ""    return crud.get_specialties(db, skip=skip, limit=limit)

@router.get("/{specialty_id}", response_model=schemas.Specialty)
def read_specialty(specialty_id: int, db: Session = Depends(get_db)):
    db_specialty = crud.get_specialty_by_id(db, specialty_id=specialty_id)
    if db_specialty is None:
        raise HTTPException(status_code=404, detail="Specialty not found")
    return db_specialty

@router.put("/{specialty_id}", response_model=schemas.Specialty)
def update_specialty(specialty_id: int, specialty: schemas.SpecialtyUpdate, db: Session = Depends(get_db)):
    db_specialty = crud.update_specialty(db, specialty_id=specialty_id, specialty_update=specialty)
    if db_specialty is None:
        raise HTTPException(status_code=404, detail="Specialty not found")
    return db_specialty

@router.post("/{specialty_id}/prices", response_model=schemas.Specialty)
def add_new_specialty_price(specialty_id: int, price: schemas.SpecialtyPriceCreate, db: Session = Depends(get_db)):
    db_specialty = crud.add_specialty_price(db, specialty_id=specialty_id, price_create=price)
    if db_specialty is None:
        raise HTTPException(status_code=404, detail="Specialty not found")
    return db_specialty
