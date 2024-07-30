from datetime import datetime

from typing_extensions import Annotated, Optional

from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_type.id"))

    user_type = relationship("UserType", back_populates="user")
    user_type = relationship("Trash", back_populates="user")


class UserType(Base):
    __tablename__ = "user_type"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str]

    user = relationship("User", back_populates="user_type")


class Trash(Base):
    __tablename__ = "user"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    created_user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime]
    cleaned_user_id: Optional[Mapped[str]] = mapped_column(ForeignKey("user.id"))
    cleaned_at: Optional[Mapped[datetime]]
    location_x: Mapped[float]
    location_y: Mapped[float]
    status_id: Mapped[int] = mapped_column(ForeignKey("trash_type.id"))
    severity_id: Mapped[int] = mapped_column(ForeignKey("severity.id"))
    image_url: Optional[Mapped[str]]
    description: Mapped[str]

    user_type = relationship("User", back_populates="trash")
    user_type = relationship("TrashType", back_populates="trash")


class TrashType(Base):
    __tablename__ = "trash_type"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str]

    user = relationship("Trash", back_populates="trash_type")


class Status(Base):
    __tablename__ = "status"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str]

    user = relationship("Trash", back_populates="status")


class Severity(Base):
    __tablename__ = "severity"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str]

    user = relationship("Trash", back_populates="status")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    print(CreateTable(User.__table__))
