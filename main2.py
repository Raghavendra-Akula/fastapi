from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List

Books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher": "Scribner",
        "published_date": "1925-04-10",
        "page_count": 218,
        "language": "English"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publisher": "J.B. Lippincott & Co.",
        "published_date": "1960-07-11",
        "page_count": 281,
        "language": "English"
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "publisher": "Secker & Warburg",
        "published_date": "1949-06-08",
        "page_count": 328,
        "language": "English"
    },
    {
        "id": 4,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "publisher": "T. Egerton",
        "published_date": "1813-01-28",
        "page_count": 279,
        "language": "English"
    },
    {
        "id": 5,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "publisher": "Little, Brown and Company",
        "published_date": "1951-07-16",
        "page_count": 214,
        "language": "English"
    },
    {
        "id": 6,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "publisher": "George Allen & Unwin",
        "published_date": "1937-09-21",
        "page_count": 310,
        "language": "English"
    }
]

class Book (BaseModel):
    id: int   
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

app = FastAPI()
@app.get("/books", response_model=List[Book])
async def get_all_books():
    return Books

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    Books.append(new_book)
    return new_book

@app.get("/books/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in Books:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Book not found"
        )

@app.patch("/books/{book_id}")
async def update_book(book_id: int, update_book: updateBookModel) -> dict:
    for book in Books:
        if book["id"]== book_id:
            book["title"] = update_book.title
            book["author"] = update_book.author
            book["publisher"] = update_book.publisher
            book["page_count"] = update_book.page_count
            book["language"] = update_book.language
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Book not found"
        )

@app.delete("/books/{book_id}")
async def delete_book(book_id: int) -> dict:
    for book in Books:
        if book["id"]== book_id:
            Books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Book not found"
        )
    
