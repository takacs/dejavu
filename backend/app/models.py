from datetime import datetime
from typing_extensions import Annotated, Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    created_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_type.id"))

    user_type = relationship("UserType", back_populates="user")
    created_trash = relationship(
        "Trash", back_populates="created_user", foreign_keys="[Trash.created_user_id]"
    )
    cleaned_trash = relationship(
        "Trash", back_populates="cleaned_user", foreign_keys="[Trash.cleaned_user_id]"
    )


class UserType(Base):
    __tablename__ = "user_type"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str]

    user = relationship("User", back_populates="user_type")


class Trash(Base):
    __tablename__ = "trash"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    created_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_date: Mapped[datetime] = mapped_column(default=func.now())
    cleaned_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user.id"), nullable=True
    )
    cleaned_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    location_x: Mapped[float]
    location_y: Mapped[float]
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    severity_id: Mapped[int] = mapped_column(ForeignKey("severity.id"))
    trash_type_id: Mapped[int] = mapped_column(ForeignKey("trash_type.id"))
    description: Mapped[str]

    created_user = relationship(
        "User", back_populates="created_trash", foreign_keys=[created_user_id]
    )
    cleaned_user = relationship(
        "User", back_populates="cleaned_trash", foreign_keys=[cleaned_user_id]
    )
    trash_type = relationship("TrashType", back_populates="trash")
    severity = relationship("Severity", back_populates="trash")
    status = relationship("Status", back_populates="trash")


class TrashType(Base):
    __tablename__ = "trash_type"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str]

    trash = relationship("Trash", back_populates="trash_type")


class Status(Base):
    __tablename__ = "status"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str]

    trash = relationship("Trash", back_populates="status")


class Severity(Base):
    __tablename__ = "severity"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str]

    trash = relationship("Trash", back_populates="severity")
