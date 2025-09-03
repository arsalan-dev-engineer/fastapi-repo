from fastapi import FastAPI

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


@app.get("/")
async def landing_page():
    return {"message": "Welcome"}


@app.get("/books")
async def get_all_books():
    return BOOKS


@app.get("/books/{title}")
async def get_book(title: str):
    for book in BOOKS:
        if book["title"].lower() == title.lower():
            return book
    return {"error": "Book not found"}
 