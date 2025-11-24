from fastapi import FastAPI
from app.api.v1.routes import book

version = "v1"


app = FastAPI(
    title="Book Management API",
    description="API for managing a collection of books.",
    version="1.0.0"
)


app.include_router(book.book_router, prefix=f"/api/{version}")
