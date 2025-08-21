from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# In-memory "database"
users_db = {}


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request,
                email: str = Form(...),
                password: str = Form(...)):
    user = users_db.get(email)
    if user and user.password == password:
        # Redirect to dashboard with user's name
        response = RedirectResponse(url="/dashboard", status_code=303)
        return response
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Invalid credentials"
    })


@router.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
async def signup(
    request: Request,
    fname: str = Form(...),
    lname: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    password: str = Form(...),
):
    if email in users_db:
        return templates.TemplateResponse("signup.html",
                                          {"request": request,
                                           "error": "Email already registered"
                                           })

    new_user = User(fname=fname, lname=lname, email=email,
                    mobile=mobile, password=password)
    users_db[email] = new_user

    # After signup, redirect to login
    response = RedirectResponse(url="/login", status_code=303)
    return response


@router.get("/dashboard")
async def dashboard(request: Request):
    # Just a placeholder: you’d normally use sessions/tokens
    return templates.TemplateResponse("dashboard.html",
                                      {"request": request,
                                       "user_name": "Test User"
                                       })
