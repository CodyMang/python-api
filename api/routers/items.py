from .. import schemas, database
from api.crud import item_crud,token_crud
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from os.path import exists

router = APIRouter()


@router.get("/items/{item_id}", response_model=list[schemas.Item])
async def read_items(id:int, db: Session = Depends(database.get_db)):
    items = item_crud.get_item_by_id(db, id)
    return items

  

@router.get("/items/", response_model=schemas.ResponseListItem)
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    items = item_crud.get_items(db, skip=skip, limit=limit) 

    return schemas.ResponseListItem(data=items)


@router.get("/images/{image_id}")
async def read_items(image_id:str, db: Session = Depends(database.get_db)):    
    item_url = item_crud.get_user_item_by_path(db,image_id)
    if not item_url:
        raise HTTPException(status_code=404, detail=f"Could not find image with id: {image_id}")
    return FileResponse(f'./{item_url}',media_type='png')


@router.post("/items/create", response_model=schemas.ResponseItem )
async def create_item_for_user(
    item: schemas.ItemCreate, db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(token_crud.get_current_active_user)
):
    new_item = item_crud.create_user_item(db=db, item=item, user_id=current_user.id)
    if new_item:
        response = schemas.ResponseItem(data=new_item)
        return response
    else: 
        raise HTTPException(status_code=400, detail="Prompt is not accepted")
