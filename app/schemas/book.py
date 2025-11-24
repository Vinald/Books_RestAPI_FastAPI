from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: str
    pages: int
    language: str


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    pages: int
    language: str


class BookInDB(BookBase):
    id: int

    class Config:
        orm_mode = True


class BookOut(BookInDB):
    pass