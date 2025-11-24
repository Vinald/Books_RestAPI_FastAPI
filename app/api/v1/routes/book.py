from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from app.schemas.book import BookCreate, BookOut, BookUpdate
from typing import List

book_router = APIRouter(
    tags=["Books"],
    prefix="/books"
)

BOOKS_DB = [
    {
        "id": 1,
         "title": "Book 1",
         "author": "Author 1",
         "publisher": "Publisher 1",
         "publish_date": "2020-01-01",
         "pages": 300,
         "language": "English"
    },
    {
         "id": 2,
         "title": "Book 2",
         "author": "Author 2",
         "publisher": "Publisher 2",
         "publish_date": "2021-02-02",
         "pages": 250,
         "language": "English"},
    ]

@book_router.get("/", response_model=List[BookOut], status_code=status.HTTP_200_OK)
async def get_books() -> List[BookOut]:
    return BOOKS_DB


@book_router.get("/{book_id}", response_model=BookOut, status_code=status.HTTP_200_OK)
async def get_book(book_id: int) -> BookOut | dict:
    for book in BOOKS_DB:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate) -> dict:
    new_book = book.model_dump()
    new_book["id"] = len(BOOKS_DB) + 1
    BOOKS_DB.append(new_book)
    return {"message": f"Book '{book.title}' by {book.author} created successfully!"}


@book_router.patch("/{book_id}", response_model=BookOut, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_update_data: BookUpdate) -> dict:
    for book in BOOKS_DB:
        if book["id"] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['publisher'] = book_update_data.publisher
            book['pages'] = book_update_data.pages
            book['language'] = book_update_data.language
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for index, book in enumerate(BOOKS_DB):
        if book["id"] == book_id:
            BOOKS_DB.pop(index)
            return {"message": f"Book with id {book_id} deleted successfully!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")