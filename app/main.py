from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BookCreateModel(BaseModel):
    title: str
    author: str


@app.get("/books")
async def get_books():
    return {"books": ["Book 1", "Book 2", "Book 3"]}

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    return {"book_id": book_id, "title": f"Book {book_id}", "author": "Author Name"}


@app.post("/book")
async def create_book(book: BookCreateModel):
    return {"message": f"Book '{book.title}' by {book.author} created successfully!"}