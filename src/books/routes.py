from fastapi import APIRouter
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from src.books.book_data import Books
from src.books.schemas import Book,updateBookModel
from typing import List

book_router = APIRouter()



@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return Books

@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    Books.append(new_book)
    return new_book

@book_router.get("/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in Books:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Book not found"
        )

@book_router.patch("/{book_id}")
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

@book_router.delete("/{book_id}")
async def delete_book(book_id: int) -> dict:
    for book in Books:
        if book["id"]== book_id:
            Books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Book not found"
        )
    
