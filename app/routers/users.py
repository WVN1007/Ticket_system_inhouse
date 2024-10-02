"""Router to Users data"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app import schemas, utils
from app.database import get_db

import app.db_model as models
import uuid

router = APIRouter(
    prefix="/api", tags=["users"], responses={404: {"description": "Not found"}}
)


@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """create a new user"""
    hashed_pwd = utils.hash_pwd(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/", response_model=list[schemas.UserOut])
async def read_users(db: Session = Depends(get_db)):
    """Get all users, NOTE: ADMIN only"""
    users = db.execute(select(models.User)).scalars().all()
    return users

@router.put("/users/{id}", response_model=schemas.UserOut)
async def update_user_w_id(
    id: str, update_user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    """update the user with put method"""
    try:
        uid = uuid.UUID(id)
        user = db.execute(select(models.User).filter_by(uid=uid)).scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        update_dict = dict(update_user)
        db.execute(update(models.User).where(models.User.uid==uid).values(**update_dict))
        db.commit()
        db.refresh(user)
    except Exception as e:
        raise e
    return user


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(id:str, db: Session = Depends(get_db)):
    '''Delete a User in the database: UNSAFE'''
    uid = uuid.UUID(id)
    user = db.execute(select(models.User).filter_by(uid=uid)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.execute(delete(models.User).where(models.User.uid==uid))
    db.commit()
    return {"msg":"UserDeleted"}

@router.get("/users/{uid}", response_model=schemas.UserOut)
async def read_user(uid: str, db: Session = Depends(get_db)):
    id = uuid.UUID(uid)
    user = db.execute(select(models.User).filter_by(uid=id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
