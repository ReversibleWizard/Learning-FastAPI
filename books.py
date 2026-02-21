from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'history'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'maths'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'economics'},
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{dynamic_params}")
async def read_all_books(dynamic_params: str):
    print(dynamic_params.casefold())
    return [BOOK for BOOK in BOOKS if BOOK.get('category').casefold() == dynamic_params.casefold()]

@app.get("/book/{dynamic_params}")
async def read_books(dynamic_params: str, category: str):
    print(dynamic_params.casefold())
    return [BOOK for BOOK in BOOKS if (BOOK.get('category').casefold() == category.casefold()
                                       and BOOK.get('title').casefold() == dynamic_params.casefold())]


@app.post("/books")
async def create_Book(new_Book=Body()):
    BOOKS.append(new_Book)

@app.put("/books")
async def update_Book(updates_books=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updates_books.get('title').casefold():
            BOOKS[i] = updates_books

@app.delete("/books/{book_title}")
async def delete_Book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)

# @app.get("/book/{author}")
# async def get_bookByAuthor(author: str):
#     books_to_be_returned = []
#     for book in BOOKS:
#         if book.get('author').casefold() == author.casefold():
#             books_to_be_returned.append(book)
#     return books_to_be_returned

@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return