"""Router to Users data"""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
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


@router.get("/devs/{uid}", response_model=schemas.DevOut)
async def read_user(uid: str, db: Session = Depends(get_db)):
    id = uuid.UUID(uid)
    staff = db.execute(select(models.Dev).filter_by(uid=id)).scalar_one_or_none()
    if staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return staff


@router.put("/devs/{uid}", response_model=schemas.DevOut)
async def update_dev_w_id(
    uid: str, update_dev: schemas.DevUpdate, db: Session = Depends(get_db)
):
    """update the user with put method"""
    try:
        uid = uuid.UUID(uid)
        dev = db.execute(select(models.Dev).filter_by(uid=uid)).scalar_one_or_none()
        if dev is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        update_dict = dict(update_dev)
        db.execute(
            update(models.Dev).where(models.Dev.uid == uid).values(**update_dict)
        )
        db.commit()
        db.refresh(dev)
    except Exception as e:
        raise e
    return dev


@router.delete("/devs/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_dev(id: str, db: Session = Depends(get_db)):
    """Delete a Dev in the database: UNSAFE"""
    uid = uuid.UUID(id)
    staff = db.execute(select(models.Dev).filter_by(uid=uid)).scalar_one_or_none()
    if staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.execute(delete(models.Dev).where(models.Dev.uid == uid))
    db.commit()
    return {"msg": "UserDeleted"}
