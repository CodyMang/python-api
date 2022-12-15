from sqlalchemy.orm import Session
from api.auth.password import get_password_hash, verify_password
from .. import models, schemas
from .token_crud import oauth2_scheme, create_access_token

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
    :param username: The User Username.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate(db_session: Session, username: str, password: str):
    user = get_user_by_username(db_session, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

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
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(
        data={"sub": db_user.username}
    )
    

    new_user = schemas.UserWithToken(
        username=db_user.username, 
        access_token=access_token,
        token_type= "bearer"
    )
    return new_user    





