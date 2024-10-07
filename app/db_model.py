""" database tables models"""

import enum
from sqlalchemy import ForeignKey, String
from .database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import Literal, Optional, List


# set Enum classes
# class Status(enum.Enum):
#     ACTIVE = "0"
#     NEW = "1"
#     CLOSE = "2"

Status = Literal["0","1","2"]

# class Severity(enum.Enum):
#     LOW = "1"
#     MEDIUM = "2"
#     HIGH = "3"
Severity = Literal["1","2","3"]

# class State(enum.Enum):
#     DRAFT = "0"
#     SUBMITTED = "1"
State = Literal["0","1"]

# class Typ(enum.Enum):
#     INC = "INC"
#     RITM = "SR"  # change in SR
Typ = Literal["INC","SR"]

# class UserRole(enum.Enum):
#     ADMIN = "admin"
#     USER = "user"
#
UserRole = Literal["ADMIN","USER"]

# class DevRole(enum.Enum):
#     ADMIN = "admin"
#     STAFF = "staff"

DevRole = Literal["ADMIN","STAFF"]

class Ticket(Base):
    __tablename__ = "ticket_table"

    typ: Mapped[Typ]
    status: Mapped[Status]
    state: Mapped[State]
    severity: Mapped[Severity]
    # one tomany relationship with User
    # when a user is deleted, the ticket still persits
    # but the owner will be set to 'NULL'
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_table.uid", ondelete="SET NULL")
    )
    owner: Mapped["User"] = relationship("User", back_populates="tickets")
    # one to one with dev staffs
    # but set it as optional to indicate we can designate or not
    assign_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("dev_table.uid", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    assign_to: Mapped[Optional["Dev"]] = relationship(
        back_populates="assigned_tickets",
        foreign_keys=[assign_to_id],
        default=None,
    )

    uid: Mapped[uuid.UUID] = mapped_column(
        default_factory=uuid.uuid4, primary_key=True
    )
    create_date: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc)
    )
    update_date: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )
    description: Mapped[str] = mapped_column(
        String, default="no description given"
    )

    def __repr__(self) -> str:
        return f"""
        TICKET(
        id={self.uid!r},
        type={self.typ!r},
        status={self.status!r},
        state={self.state!r},
        create_date={self.create_date},
        update_date={self.update_date!r},
        description={self.description!r})"""


class User(Base):
    __tablename__ = "user_table"

    username: Mapped[str] = mapped_column(String(16), unique=True)
    role: Mapped[UserRole]
    # many to one relationship with ticket
    tickets: Mapped[Optional[List["Ticket"]]] = relationship(
        "Ticket",
        back_populates="owner",
        cascade="all, delete",
        passive_deletes=True,
    )
    password: Mapped[bytes]
    uid: Mapped[uuid.UUID] = mapped_column(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(
        String,
        default="example@example.com",
        unique=True,
    )

    def __repr__(self) -> str:
        return f"Table=User,id={self.uid.hex},role={self.role.value},username={self.username!r},email={self.email!r}"


class Dev(Base):
    __tablename__ = "dev_table"

    username: Mapped[str] = mapped_column(
        String(16),
        unique=True,
    )
    password: Mapped[bytes]
    # set relationship with tickets
    assigned_tickets: Mapped[Optional[List["Ticket"]]] = relationship(
        back_populates="assign_to"
    )
    role: Mapped[DevRole]
    email: Mapped[str] = mapped_column(String, unique=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        default_factory=uuid.uuid4, primary_key=True
    )

    def __repr__(self) -> str:
        return f"Table=Dev,id={self.uid.hex},role={self.role.value},username={self.username!r},email={self.email!r}"


class Attachment(Base):
    __tablename__ = "attachment_table"

    name: Mapped[str] = mapped_column(String, nullable=False)
    path: Mapped[str] = mapped_column(String)
    upload_date: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc)
    )
    uid: Mapped[uuid.UUID] = mapped_column(
        default_factory=uuid.uuid4, primary_key=True
    )

    def __repr__(self) -> str:
        return f"Attachment(id={self.uid!r},Upload_date={self.upload_date!r},name={self.name!r},path={self.path!r})"
