from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth import router as auth_router
from app.users import router as users_router
from app.config import settings


# Initialize FastAPI app
app = FastAPI(title=settings.app_name, debug=settings.debug)

# CORS Middleware (for frontend integration/testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Home page
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "title": "Login Web App"
                                       })


# Routers
app.include_router(auth_router)
app.include_router(users_router)


# Custom error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={
        "message": "Page not found!"
    })


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    return JSONResponse(status_code=500, content={
        "message": "Internal server error!"
    })
