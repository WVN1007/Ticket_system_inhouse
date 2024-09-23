"""schema validation using pydantic"""

from pydantic import BaseModel, EmailStr
from typing import Literal

class UserOut(BaseModel):
    """User data output when requested"""

    username: str
    role: Literal["user","admin"]
    email: EmailStr
    uid: str


class UserCreate(BaseModel):
    """User data for create a new user"""

    username: str
    role: Literal["user","admin"]
    email: EmailStr


class UserLogin(BaseModel):
    """User login models"""

    email: EmailStr
    password: str


class DevOut(BaseModel):
    """Staff data when requested"""

    username: str
    role: Literal["staff","admin"]
    email: EmailStr
    uid: str


class DevCreate(BaseModel):
    """Devs data for create a new dev"""

    username: str
    role: Literal["staff","admin"]
    email: EmailStr


class DevLogin(BaseModel):
    """Devs login pydantic models"""

    email: EmailStr
    password: str

class TicketBase(BaseModel):
    typ: Literal['INC','RITM']
    status: Literal['0','1','2']
    state: Literal['0','1']
    severity: Literal['1','2','3']
    description: str


class TicketCreate(TicketBase):
    pass
    
