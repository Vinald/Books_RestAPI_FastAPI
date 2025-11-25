from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.book import BookCreate, BookUpdate
from sqlmodel import select, desc
from app.models.book import Book
from fastapi import HTTPException, status
from datetime import date

class BookService:
    @staticmethod
    async def get_all_books(session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        results = await session.exec(statement)
        books = results.all()
        return books

    @staticmethod
    async def get_book(book_uuid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uuid)
        results = await session.exec(statement)
        book = results.first()
        return book if book else None

    @staticmethod
    async def create_book(book_data: BookCreate, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        book_data_dict.publish_date = date.strftime(book_data_dict['publish_date'], '%Y-%m-%d')
        new_book = Book(**book_data_dict)
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book


    async def update_book(
        self, book_uuid: str, update_data: BookUpdate, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uuid, session)

        if not book_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_uuid} not found")

        update_data_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)
        session.add(book_to_update)
        await session.commit()
        await session.refresh(book_to_update)
        return book_to_update


    async def delete_book(self, book_uuid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uuid, session)

        if not book_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_uuid} not found")

        await session.delete(book_to_delete)
        await session.commit()
        return {"message": f"Book {book_uuid} deleted successfully"}
