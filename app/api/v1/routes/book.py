from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.book import BookCreate, BookOut, BookUpdate
from typing import List
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.book_service import BookService

book_router = APIRouter(
    tags=["Books"],
    prefix="/books"
)

book_service = BookService()


@book_router.get("/", response_model=List[BookOut], status_code=status.HTTP_200_OK)
async def get_books(session: AsyncSession = Depends(get_session)) -> List[BookOut]:
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/{book_id}", response_model=BookOut, status_code=status.HTTP_200_OK)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> BookOut | dict:
    book = await book_service.get_book(book_uid, session)
    return book


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookCreate)
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book, session)
    return new_book


@book_router.patch("/{book_id}", response_model=BookOut, status_code=status.HTTP_200_OK)
async def update_book(book_uid: str, book_update_data: BookUpdate, session: AsyncSession = Depends(get_session)) -> BookOut:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    return updated_book


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_book(book_uid, session)
    return deleted_book