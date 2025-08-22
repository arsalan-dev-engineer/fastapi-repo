from fastapi import APIRouter
from .database import users_db
from .models import User

router = APIRouter()


@router.get("/users", response_model=list[User])
async def list_users():
    return users_db
