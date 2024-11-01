from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    name: str
    address: str
    phone: str
    email: str
    registration_date: date
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

class BookBase(BaseModel):
    title: str
    author: str
    category: str
    publication_year: int
    status: str
    type: str
    publisher_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class LoanBase(BaseModel):
    book_id: int
    user_id: int
    loan_date: date
    return_date: date
    renewals: int
    status: str
    librarian_id: int

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int

    class Config:
        orm_mode = True

class EventRegistrationCreate(BaseModel):
    event_id: int
    user_id: int
    registration_date: date

class EventRegistration(EventRegistrationCreate):
    id: int

    class Config:
        orm_mode = True