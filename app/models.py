# app/schemas.py

from pydantic import BaseModel
from datetime import date  # Cambiado de datetime a date

class UserBase(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    registration_date: date  # Cambiado de datetime a date
    user_type: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
class FineCreate(BaseModel):
    user_id: int
    reason: str
    start_date: date
    end_date: date
    amount: float

class Fine(FineCreate):
    id: int
    user_id: int

class PublisherBase(BaseModel):
    publisher_name: str
    country: str
    foundation_year: int

class PublisherCreate(PublisherBase):
    pass

class Publisher(PublisherBase):
    id: int

    class Config:
        orm_mode = True

class EventBase(BaseModel):
    event_name: str
    description: str
    event_date: date
    event_type: str
    capacity: int

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    class Config:
        orm_mode = True