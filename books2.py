from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1949, lt=2027)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "New Author",
                "description": "A new description of the book",
                "rating": 5,
                "published_date": 2024
            }
        }
    }

BOOKS = [
    Book(1, "Computer Science", "Coding with Roby", "A very nice book", 5, 2010),
    Book(2, "Be fast with fast api", "Sayak", "A very great book", 5,2010),
    Book(3, "Master Endpoints", "Coding with Roby", "A awesome book", 5, 2011),
    Book(4, "HP1", "Joe", "A very nice book", 1, 1999),
    Book(5, "HP2", "Andrew", "A very nice book", 3, 2000),
    Book(6, "HP3", "Iman", "A very nice book", 4,2025),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return

@app.get("/books_by_published_date/")
async def read_book_by_published_date(book_published_date: int):
    book_to_return = []
    for book in BOOKS:
        if book.published_date == book_published_date:
            book_to_return.append(book)
    return book_to_return

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump()) # for pydantic use .dict() and for pydantic2 use model_dump()
    # print(type(new_book))
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

@app.put("/books/update_book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
