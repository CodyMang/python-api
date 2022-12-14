from .. import schemas, database
from api.crud import item_crud,token_crud
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/items/{item_id}", response_model=list[schemas.Item])
async def read_items(id:int, db: Session = Depends(database.get_db)):
    items = item_crud.get_item_by_id(db, id)
    return items

  
@router.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    items = item_crud.get_items(db, skip=skip, limit=limit)
    return items

@router.post("/items/create", response_model=schemas.Item )
async def create_item_for_user(
    item: schemas.ItemCreate, db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(token_crud.get_current_active_user)
):
    return item_crud.create_user_item(db=db, item=item, user_id=current_user.id)
