from .. import schemas, database
from api.crud import item_crud
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/items/{item_id}", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    items = item_crud.get_items(db, skip=skip, limit=limit)
    return items

  
@router.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    items = item_crud.get_items(db, skip=skip, limit=limit)
    return items
