"""
This Python file is the backend for index.html
Once a form is submitted, FastAPI should receive the resources
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI instance
app = FastAPI()

# Enable CORS so the frontend (index.html) can call this backend
# Without this, browsers would block requests if the HTML is opened locally
app.add_middleware(
    CORSMiddleware,
    # Allow requests from any origin (use specific domains in production)
    allow_origins=["*"],
    allow_credentials=True,
    # Allow all HTTP methods: GET, POST, PUT, DELETE...
    allow_methods=["*"],
    allow_headers=["*"],      # Allow all headers
)


# Define a request body model using Pydantic
# This describes what data the backend expects from the form
class FormRequest(BaseModel):
    fname: str
    lname: str
    email: str
    mobile: str


# In-memory database (list)
# This stores submitted form data temporarily in memory
# (will reset every time the server restarts)
forms: List[FormRequest] = []


# Root endpoint - just a test route
@app.get("/")
async def index():
    return {"message": "welcome to form app"}


# GET endpoint to fetch all submitted forms
# Returns the list of forms in memory
@app.get("/forms/", response_model=List[FormRequest])
async def get_all_forms():
    return forms


# POST endpoint to accept form submissions
# Takes FormRequest (JSON body) and appends it to the in-memory list
@app.post("/forms/", response_model=FormRequest)
async def create_form(form: FormRequest):
    forms.append(form)
    return form
