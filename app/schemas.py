"""schema validation using pydantic"""

from datetime import datetime
from pydantic import BaseModel, EmailStr , Field
from typing import Literal, List, Optional
import uuid


class UserOut(BaseModel):
    """User data output when requested"""

    username: str
    role: str
    email: EmailStr
    uid: uuid.UUID
    tickets: Optional[list] = []

class UserUpdate(BaseModel):
    """User data just for updates"""
    username: str
    role: str
    email: EmailStr

class UserCreate(BaseModel):
    """User data for create a new user"""

    username: str
    role: Literal["USER", "ADMIN"]
    email: EmailStr
    password: str
    tickets: Optional[list]= []


class UserLogin(BaseModel):
    """User login models"""

    email: EmailStr
    password: str


class DevOut(BaseModel):
    """Staff data when requested"""

    username: str
    role: str
    email: EmailStr
    uid: uuid.UUID
    assigned_tickets: Optional[list] = []


class DevCreate(BaseModel):
    """Devs data for create a new dev"""

    username: str
    role: Literal["STAFF", "ADMIN"]
    email: EmailStr
    password: str
    assigned_tickets: List[None] = []

class DevLogin(BaseModel):
    """Devs login pydantic models"""

    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")

class TicketBase(BaseModel):
    typ: Literal["INC", "RITM"]
    status: Literal["0", "1", "2"]
    state: Literal["0", "1"]
    severity: Literal["1", "2", "3"]
    description: str


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    uid: uuid.UUID
    create_at: datetime
    owner_id: uuid.UUID
    owner: UserOut
    assign_to_id: uuid.UUID | None = None
    assign_to: DevOut | None = None


class TicketOut(BaseModel):
    Ticket: Ticket
    update_date: datetime
