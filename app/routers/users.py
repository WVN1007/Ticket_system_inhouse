"""Router to Users data"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import schemas, utils
from app.database import get_db
import app.db_model as models

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


@router.get("/users/")
async def read_users(db: Session = Depends(get_db)):
    """Get all users, NOTE: ADMIN only"""
    users = db.execute(select(models.User)).scalars().all()

    # serialize result in a dictionary type
    string_user = list(str(user) for user in users)
    mapped_users = map(utils.serialize, list(string_user))

    re = {}
    re["details"] = list(mapped_users)
    return re


@router.get("/users/me")
async def read_current_user():
    """Get current logged in user"""
    return {"myuid": "my fakeuid"}


@router.get("/users/{uid}")
async def read_user(uid: str):
    return {f"{uid}": "fake_uid", "fake": "fasle user"}
