# to know information format which UI can send to API we are defining this schemas format to capture it easily and send back to UI properly.

from pydantic import BaseModel
import uuid
from datetime import datetime, date
from typing import List
from src.reviews.schemas import ReviewModel

class Book (BaseModel):
    uid: uuid.UUID  
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime 
    updated_at : datetime
    user_uid : uuid.UUID | None

class BookDetail(Book):
    reviews: List[ReviewModel]


class BookCreateModel (BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

class updateBookModel (BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
