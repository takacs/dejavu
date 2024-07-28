import datetime
from pydantic import BaseModel
from typing import Optional


class Status(BaseModel):
    id: int
    name: str


class Severity(BaseModel):
    id: int
    name: str


class UserType(BaseModel):
    id: int
    name: str


class TrashType(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    username: str
    email: str
    user_type_id: int


class TrashCreate(BaseModel):
    created_by: str
    created_at: datetime.datetime
    location_x: float
    location_y: float
    trash_type_id: int
    status_id: int
    severity_id: int
    image_url: str
    description: str


class Trash(TrashCreate):
    cleaned_by: Optional[str]
    cleaned_at: Optional[datetime.datetime]
    id: Optional[int]


class Cleaner(BaseModel):
    cleaned_by: str
    cleaned_at: datetime.datetime
