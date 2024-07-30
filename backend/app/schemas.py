from enum import Enum
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class Status(Enum):
    Success = "Success"
    Failed = "Failed"


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    username: str
    email: str
    user_type_id: int
    created_date: datetime


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


class TrashBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    created_user_id: int
    created_date: datetime
    location_x: float
    location_y: float
    status_id: int
    severity_id: int
    trash_type_id: int
    description: str


class TrashResponse(BaseModel):
    Status: Status
    Trash: TrashBaseSchema


class GetTrashResponse(BaseModel):
    Status: Status
    Trash: TrashBaseSchema


class ListTrashResponse(BaseModel):
    status: Status
    results: int
    trash: List[TrashBaseSchema]


class DeleteTrashResponse(BaseModel):
    Status: Status
    Message: str
