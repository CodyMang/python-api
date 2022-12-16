from .. import schemas, database
import os
from api.crud import user_crud,token_crud
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv(".env")

# Get the value of the "SECRET_KEY" variable
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10000 # about a week

router = APIRouter()

@router.post("/users/", response_model=schemas.UserWithToken)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    return user_crud.create_user(db=db, user=user)


@router.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/token/", response_model=schemas.ResponseToken)
async def login_for_access_token(user:schemas.UserCreate, db:Session = Depends(database.get_db)):
    user = user_crud.authenticate(db, user.username, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token_crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token_response = schemas.ResponseToken(data=schemas.Token(access_token= access_token,token_type= "bearer"))
    return token_response


@router.get("/auth/", response_model=schemas.ResponseAuth)
async def read_users_me(current_user: schemas.User = Depends(token_crud.get_current_active_user)):
    return schemas.ResponseAuth(success=True)
