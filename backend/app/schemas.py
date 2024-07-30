from enum import Enum
from datetime import datetime
from typing import List
from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    id: int
    username: str
    email: str
    user_type_id: int
    create_date: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class Status(Enum):
    Success = "Success"
    Failed = "Failed"


class UserResponse(BaseModel):
    Status: Status
    User: UserBaseSchema


class GetUserResponse(BaseModel):
    Status: Status
    User: UserBaseSchema


class ListUserResponse(BaseModel):
    status: Status
    results: int
    users: List[UserBaseSchema]


class DeleteUserResponse(BaseModel):
    Status: Status
    Message: str
