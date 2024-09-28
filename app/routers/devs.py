"""Router to Users data"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app import schemas, utils
from app.database import get_db
import app.db_model as models
import uuid

router = APIRouter(
    prefix="/api", tags=["devs"], responses={404: {"description": "Not found"}}
)


@router.post(
    "/devs/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DevOut,
)
async def create_user(dev: schemas.DevCreate, db: Session = Depends(get_db)):
    """create a new dev"""
    hashed_pwd = utils.hash_pwd(dev.password)
    dev.password = hashed_pwd
    new_staff = models.Dev(**dev.model_dump())

    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff


@router.get("/devs/", response_model=list[schemas.DevOut])
async def read_devs(db: Session = Depends(get_db)):
    """Get all devs, NOTE: ADMIN only"""
    staffs = db.execute(select(models.Dev)).scalars().all()
    return staffs


# TODO: add method to get current login staff data
# @router.get("/devs/me")
# async def read_current_user():
#     """Get current logged in dev"""
#     return {"myuid": "my fakeuid"}

# TODO: add method to update staff data


@router.get("/devs/{uid}", response_model=schemas.DevOut)
async def read_user(uid: str, db: Session = Depends(get_db)):
    id = uuid.UUID(uid)
    staff = db.execute(select(models.Dev).filter_by(uid=id)).scalar_one()
    return staff
