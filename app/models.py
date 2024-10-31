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