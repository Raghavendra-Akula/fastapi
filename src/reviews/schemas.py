from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
import uuid

class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    book_uid: Optional[uuid.UUID]
    user_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at : datetime

class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text : str
    