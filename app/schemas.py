"""schema validation using pydantic"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Literal, List, Optional, Union
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
    password: Union[str, bytes]
    tickets: Optional[list] = []


class UserLoggedIn(BaseModel):
    """User logged in with Tojen"""

    username: str
    email: EmailStr
    uid: uuid.UUID


class DevOut(BaseModel):
    """Staff data when requested"""

    username: str
    role: str
    email: EmailStr
    uid: uuid.UUID
    assigned_tickets: Optional[list] = []


class DevUpdate(BaseModel):
    """Dev data just for updates"""

    username: str
    role: str
    email: EmailStr


class DevCreate(BaseModel):
    """Devs data for create a new dev"""

    username: str
    role: Literal["STAFF", "ADMIN"]
    email: EmailStr
    password: Union[str, bytes]
    assigned_tickets: List[None] = []


class DevLogin(BaseModel):
    """Devs login pydantic models"""

    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TicketBase(BaseModel):
    typ: Literal["INC", "SR"]
    status: Literal["0", "1", "2"]
    state: Literal["0", "1"]
    severity: Literal["1", "2", "3"]
    description: str


class TicketCreate(TicketBase):
    assign_to_id: uuid.UUID | None = None


class Ticket(TicketBase):
    uid: uuid.UUID
    create_date: datetime
    owner_id: uuid.UUID
    assign_to_id: uuid.UUID | None = None
    model_config=ConfigDict(from_attributes=True)


class TicketOut(Ticket):
    # Ticket: Ticket
    update_date: datetime | None = None
    model_config=ConfigDict(from_attributes=True)
