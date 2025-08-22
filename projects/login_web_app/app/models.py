from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    fname: str
    lname: str
    email: EmailStr
    mobile: str
    password: str


class User(BaseModel):
    fname: str
    lname: str
    email: EmailStr
    mobile: str
    password: str
