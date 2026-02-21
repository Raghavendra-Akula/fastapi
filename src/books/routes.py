from fastapi import APIRouter
from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException
from src.books.schemas import Book,updateBookModel,BookCreateModel
from typing import List
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer, roleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(roleChecker(["admin","user"]))


@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), token_details = Depends(access_token_bearer)):
    print(token_details)
    Books = await book_service.get_all_books(session)
    return Books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), token_details = Depends(access_token_bearer)) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book

@book_router.get("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session), token_details = Depends(access_token_bearer)) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book :
        return book
    else :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )

@book_router.patch("/{book_uid}", response_model=updateBookModel, dependencies=[role_checker])
async def update_book(book_uid: str, update_book: updateBookModel, session: AsyncSession = Depends(get_session), token_details = Depends(access_token_bearer)) -> dict:
    updated_book = await book_service.update_book(book_uid, update_book, session)
    if updated_book is None :\
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
            )
    else:
        return update_book       

@book_router.delete("/{book_uid}", dependencies=[role_checker])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), token_details = Depends(access_token_bearer)) -> dict:
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
            )
    else :
        return {"message": "Book deleted successfully"}
        
    
