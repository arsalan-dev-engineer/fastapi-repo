from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

# Create an instance of the FastAPI application
app = FastAPI(title="FastAPI books app")


# Define a Pydantic model for the book data
class Books(BaseModel):
    title: str  # Title of the book
    category: str  # Category or genre of the book
    author: str  # Author of the book
    year: int  # Year the book was published
    rating: float  # Rating of the book (e.g., out of 5)


# Initialize an empty list to store book data
BOOKS = []


@app.get("/")
async def landing_page():
    return {"message": "Welcome to Books DBS"}


# Define a GET endpoint to retrieve all books
@app.get("/books")
async def get_all_books():
    # Return the list of books
    return BOOKS


# Define a GET endpoint to retrieve a book by its ID
@app.get("/books/{book_id}")
async def get_book(book_id: str):
    # Iterate through the BOOKS list to find a book with the matching book_id
    for book in BOOKS:
        if book["book_id"] == book_id:
            return book  # Return the book if found
    # If no book is found, return a 404 error with a message
    return {"error": "Book not found"}


# Define a POST endpoint to add a new book
@app.post("/books")
async def add_book(book: Books):
    # Generate a unique ID for the book using uuid4
    book_id = str(uuid4())
    # Convert the Pydantic model to a dictionary and add the generated book_id
    book_data = book.model_dump()
    book_data["book_id"] = book_id
    # Add the new book to the BOOKS list
    BOOKS.append(book_data)
    # Return a confirmation message with the added book
    return {"message": "Book added successfully", "book": book_data}
