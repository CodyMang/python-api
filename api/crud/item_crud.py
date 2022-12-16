from sqlalchemy.orm import Session
from fastapi import  HTTPException
from .. import models, schemas
from ..helpers import open_ai_interface as oai
from uuid import uuid4
from base64 import b64decode

def get_item_by_id(db: Session, id:int):
    """
    Get one item   
    :param db: The database session.
    :param int: The item id 
    """
    return db.query(models.Item).filter(models.Item.id == id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all items.
    :param db: The database session.
    :param skip: The offset used when paging.
    :param limit: The number of items to retrieve per query.
    """
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_image_url_by_id(db: Session, id:int):
    """
    Get one item image url
    :param db: The database session.
    :param int: The item url id 
    """
    return db.query(models.ItemURL).filter(models.Item.id == id).first()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """
    Create the user item.
    :param db: The database session.
    :param item: The item schema.
    :param limit: The User ID to add the item to.
    """
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    response = oai.get_images_from_desc(db_item.description).to_dict()
    if response:
        
        for obj in response['data']:
            try:
                file_id =  str(uuid4())
                file_name = f'/images/{file_id}.png'
                file_content = b64decode(obj['b64_json'])
                with open(f'.{file_name}','xb') as f:
                    f.write(file_content)
                item_url = models.ItemURL(
                    id=file_id,
                    item_id=db_item.id,
                    location=file_name
                )
                db.add(item_url)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"An error occured with OpenAI API: {e}")
    else:
        return None
    db.commit()
    db.refresh(db_item)

    return db_item



def get_user_item_by_path(db: Session, image_id:str):
    """
    Get a image by path
    """
    if image_id.endswith('.png'):
        image_id = image_id[:-4]

    item_url = db.query(models.ItemURL).filter(models.ItemURL.id == image_id).first()
    if not item_url:
        return None
    return item_url.location