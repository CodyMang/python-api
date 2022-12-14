from sqlalchemy.orm import Session
from .. import models, schemas
from ..helpers import open_ai_interface as oai


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

    for obj in response['data']:
        item_url = models.ItemURL(item_id=db_item.id,content=obj['url'])
        db.add(item_url)

    db.commit()
    db.refresh(db_item)

    return db_item