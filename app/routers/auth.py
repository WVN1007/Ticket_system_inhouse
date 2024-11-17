from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth_utils import (
    get_current_user,
    authenticate_user,
    create_access_token,
    authenticate_dev,
    get_current_staff
)
from typing import Annotated
import app.schemas as schemas
from app import settings

ACCESS_TOKEN_EXPIRE_MINUTE = settings.app_config["ACCESS_TOKEN_EXPIRE_MINUTES"]

router = APIRouter(tags=["Authentication"], prefix="/api")


@router.post("/login", response_model=schemas.Token)
async def login(
    formdata: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """user login and receive an access token"""
    # lookup the user from the formdata
    username = formdata.username
    password = formdata.password
    user = authenticate_user(usr=username, db=db, pwd=password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTE))
    access_token = create_access_token(
        data={"sub": user.username, "uid": user.uid.hex},
        expires_delta=access_token_expires,
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/devs/login", response_model=schemas.Token)
async def login(
    formdata: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """user login and receive an access token"""
    # lookup the user from the formdata
    username = formdata.username
    password = formdata.password
    dev = authenticate_dev(usr=username, db=db, pwd=password)
    if not dev:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTE))
    access_token = create_access_token(
        data={"sub": dev.username, "uid": dev.uid.hex},
        expires_delta=access_token_expires,
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/user/me", response_model=schemas.UserOut)
async def read_user(
    current_users: Annotated[schemas.UserOut, Depends(get_current_user)]
):
    return current_users

@router.get("/devs/me", response_model=schemas.DevOut)
async def read_dev(
    current_users: Annotated[schemas.DevOut, Depends(get_current_staff)]
):
    return current_users


