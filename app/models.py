# app/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    address: str
    phone: str
    email: EmailStr
    registration_date: Optional[str]  # Optional, as it might default to current date
    user_type: str

class User(UserCreate):
    id: int
