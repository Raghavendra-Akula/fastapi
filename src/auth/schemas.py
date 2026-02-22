from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import datetime
from typing import List
from src.books.schemas import Book
from src.reviews.schemas import ReviewModel

class UserCreateModel(BaseModel):
    first_name : str
    last_name : str
    username: str = Field(max_length=10)
    email: str = Field(max_length = 30)
    password : str = Field(min_length=8)
    @field_validator("password")
    def password_length_bytes(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes")
        return v

class UserModel(BaseModel):
    uid : uuid.UUID
    username: str
    email : str
    first_name : str
    last_name : str
    passwd_hash : str = Field(exclude=True)
    is_verified: bool
    created_at: datetime
    updated_at : datetime
    books: List[Book]
    reviews : List[ReviewModel]

class NewUser(BaseModel):
    uid : uuid.UUID
    username: str
    email : str
    first_name : str
    last_name : str
    passwd_hash : str = Field(exclude=True)
    is_verified: bool
    created_at: datetime


class UserLoginModel(BaseModel):
    email: str = Field(max_length = 30)
    password : str = Field(min_length=8)
