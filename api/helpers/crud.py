from sqlalchemy.orm import Session
from .. import models, schemas


def get_user(db: Session, user_id: int):
    """
    Get user by User ID.
    :param db: The database session.
    :param user_id: The User ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """
    Get user by User username.
    :param db: The database session.
    :param email: The User Username.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all users.
    :param db: The database session.
    :param skip: The offset used when paging.
    :param limit: The number of users to retrieve per query.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create user.
    :param db: The database session.
    :param user: The user schema.
    """
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Get all items.
    :param db: The database session.
    :param skip: The offset used when paging.
    :param limit: The number of items to retrieve per query.
    """
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item_by_id(db: Session, id:int):
    """
    Get one item   
    :param db: The database session.
    :param int: The item id 
    """
    return db.query(models.Item).filter(models.Item.id == id).first()


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
    return db_item
