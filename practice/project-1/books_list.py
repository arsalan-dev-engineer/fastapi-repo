from fastapi import FastAPI, Body, HTTPException

app = FastAPI()

BOOKS = [
    {"title": "Python-101", "category": "Computer Science",
        "author": "John Smith", "year": 2021, "rating": 4.5},
    {"title": "Code like a Pro", "category": "Computer Science",
        "author": "Emily Carter", "year": 2019, "rating": 4.7},
    {"title": "Doctor's Medical Guide", "category": "Medicine",
        "author": "Dr. Sarah Lee", "year": 2020, "rating": 4.8},
    {"title": "Drivers Guide", "category": "Driving",
        "author": "Mike Johnson", "year": 2018, "rating": 4.2},
    {"title": "Mastering Cloud", "category": "Technology",
        "author": "Sophia Patel", "year": 2022, "rating": 4.9},
    {"title": "History Unfolded", "category": "History",
        "author": "David Brown", "year": 2017, "rating": 4.1},
    {"title": "Cooking Made Easy", "category": "Cooking",
        "author": "Olivia Green", "year": 2023, "rating": 4.6},
    {"title": "Fitness for Life", "category": "Health",
        "author": "Chris Adams", "year": 2021, "rating": 4.4}
]


# ===================
# GET endpoint
# ===================

@app.get("/")
async def landing_page():
    return {"message": "Welcome"}


# ===================
# GET endpoint
# ===================

@app.get("/books")
async def get_all_books():
    return BOOKS


# ===================
# GET endpoint
# ===================

@app.get("/books/{title}")
async def get_book(title: str):
    for book in BOOKS:
        if book.get("title", "").casefold() == title.casefold():
            return book
    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


# ===================
# PUT endpoint
# ===================

@app.put("/books/updated_book")
async def update_book(updated_book=Body()):
    # Ensure the payload contains a "title" key
    if "title" not in updated_book:
        raise HTTPException(
            status_code=400,
            detail="The 'title' field is required to update a book.")

    # Iterate through the BOOKS list to find the book to update
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title", "").casefold() == \
                updated_book.get("title", "").casefold():
            # Update the book
            BOOKS[i].update(updated_book)
            return {"message": "Book updated successfully", "book": BOOKS[i]}

    # If no book is found, return a 404 error
    raise HTTPException(status_code=404, detail="Book not found")


# ===================
# DELETE endpoint
# ===================


@app.delete("/books/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        # compare title in case-insensitive manner
        if book.get("title", "").casefold() == book_title.casefold():
            # remove the book from the list
            BOOKS.remove(book)
            return {"message": f"Book '{book_title}' deleted successfully"}
    # if no book is found, raise a 404 error
    raise HTTPException(
        status_code=404,
        detail=f"Book '{book_title}' not found")


# ===================
# POST endpoint
# ===================

@app.post("/books")
async def create_book(new_book=Body()):
    # Ensure required keys exist
    required_fields = ["title", "category", "author", "year", "rating"]
    for field in required_fields:
        if field not in new_book:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )

    # Check for duplicates by title
    for book in BOOKS:
        if book.get("title", "").casefold() == new_book["title"].casefold():
            raise HTTPException(
                status_code=400,
                detail=f"Book '{new_book['title']}' already exists"
            )

    # Add the book
    BOOKS.append(new_book)
    return {"message": "Book added successfully", "book": new_book}