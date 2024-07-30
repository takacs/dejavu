from datetime import datetime

from typing_extensions import Annotated

from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_type.id"))

    user_type = relationship("UserType", back_populates="user")


class UserType(Base):
    __tablename__ = "user_type"

    id: Mapped[intpk]
    name: Mapped[str]

    user = relationship("User", back_populates="user_type")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable

    print(CreateTable(User.__table__))
