"""routers to tickets data"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import db_model, oauth_utils, schemas
from app.database import get_db

router = APIRouter(
    prefix="/api/tickets",
    tags=["tickets"],
    responses={404: {"description": "Not found"}},
)


@router.post("/inc", status_code=status.HTTP_201_CREATED, response_model=schemas.Ticket)
async def create_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth_utils.get_current_user),
):
    """this endpoint will create a tickets from an authenticated user"""
    new_ticket_data = ticket.model_dump()
    # print(new_ticket_data)
    try:
        user = db.execute(
            select(db_model.User).filter_by(uid=current_user.uid)
        ).scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        dev = db.execute(
            select(db_model.Dev).filter_by(uid=new_ticket_data["assign_to_id"])
        ).scalar_one_or_none()
        if dev is None:
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail="assigned resouce not found",
            )
        new_ticket_data["owner_id"] = user.uid
        new_ticket_data["owner"] = user
        new_ticket_data["assign_to_id"] = dev.uid
        new_ticket_data["assign_to"] = dev
        db_ticket = db_model.Ticket(**new_ticket_data)
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
    except Exception as e:
        # If there is any error why look up the user
        print("error from endpoint:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return db_ticket


@router.get("/", response_model=List[schemas.TicketOut])
async def get_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(oauth_utils.get_current_staff)
    or Depends(oauth_utils.get_current_user),
):
    """this endpoints will gets ticket if the login user is authenticated"""
    tickets = db.execute(select(db_model.Ticket)).scalars().all()
    return tickets


@router.get("/{id}", response_model=schemas.TicketOut)
async def get_ticket_w_id(
    id: str,
    db: Session = Depends(get_db),
    current_user=Depends(oauth_utils.get_current_user)
    or Depends(oauth_utils.get_current_staff),
):
    """retrieve specific ticket with id"""
    uid = uuid.UUID(id)
    ticket = db.execute(select(db_model.Ticket).filter_by(uid=uid)).scalar_one_or_none()
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ticket
