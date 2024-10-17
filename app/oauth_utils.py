from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import db_model
from app.database import get_db

from . import schemas, settings, utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login", scheme_name="user_oauth2")
oauth2_scheme_dev = OAuth2PasswordBearer(
    tokenUrl="/api/devs/login", scheme_name="dev_oauth2"
)

config = settings.app_config


def get_user(usr: str, db: Session):
    """utility to return a user from database"""
    user_data = db.execute(
        select(db_model.User).filter_by(username=usr)
    ).scalar_one_or_none()
    if user_data is None:
        return None
    user = schemas.UserOut(
        username=user_data.username,
        email=user_data.email,
        uid=user_data.uid,
        role=user_data.role.__str__(),
        tickets=user_data.tickets,
    )
    return user


def get_staff(usr: str, db: Session):
    """utility to return a devs from database"""
    staff_data = db.execute(
        select(db_model.Dev).filter_by(username=usr)
    ).scalar_one_or_none()
    if staff_data is None:
        return None
    user = schemas.DevOut(
        username=staff_data.username,
        email=staff_data.email,
        uid=staff_data.uid,
        role=staff_data.role.__str__(),
    )
    return user


# check user authentication
def authenticate_user(usr: str, pwd: str, db: Session):
    """check current login user is authenticated"""
    user_data = db.execute(
        select(db_model.User).filter_by(username=usr)
    ).scalar_one_or_none()
    if user_data is None:
        return None
    if utils.check_pwd(pwd, user_data.password):
        user = schemas.UserOut(
            username=user_data.username,
            email=user_data.email,
            uid=user_data.uid,
            role=user_data.role.__str__(),
        )
        return user
    return None


def authenticate_dev(usr: str, pwd: str, db: Session):
    """check current login dev is authenticated"""
    staff_data = db.execute(
        select(db_model.Dev).filter_by(username=usr)
    ).scalar_one_or_none()
    if staff_data is None:
        return None
    if utils.check_pwd(pwd, staff_data.password):
        user = schemas.UserOut(
            username=staff_data.username,
            email=staff_data.email,
            uid=staff_data.uid,
            role=staff_data.role.__str__(),
        )
        return user
    return None


# method to generate token.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """method to create access token for user"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)

    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(
        to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHMS"]
    )
    return encode_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    """get current user and check token validation"""
    # return exception
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, key=config["SECRET_KEY"], algorithms=config["ALGORITHMS"]
        )
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credential_exception

    # get user from token token_data
    user = get_user(usr=token_data.username, db=db)
    return user


async def get_current_staff(
    token: Annotated[str, Depends(oauth2_scheme_dev)], db: Session = Depends(get_db)
):
    """Get the current login staff"""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, key=config["SECRET_KEY"], algorithms=config["ALGORITHMS"]
        )
        username = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credential_exception

    staff = get_staff(usr=token_data.username, db=db)
    return staff
