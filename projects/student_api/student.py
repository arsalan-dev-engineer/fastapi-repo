from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, EmailStr, conint, constr
from typing import List, Optional, Annotated
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum
import re

app = FastAPI()


# =====================
# Gender Enum
# =====================
class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"


# =====================
# Input model for creating a student
# =====================
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    age: Annotated[int, conint(gt=18)]
    gender: GenderEnum
    phone: Annotated[str, constr(pattern=r"^\+?\d{7,15}$")]


# =====================
# Input model for updating a student
# =====================
class StudentUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    age: Optional[Annotated[int, conint(gt=18)]]
    gender: Optional[GenderEnum]
    phone: Optional[Annotated[str, constr(pattern=r"^\+?\d{7,15}$")]]


# =====================
# Full student model
# Soft delete via is_active
# =====================
class Student(StudentCreate):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True


# =====================
# In-memory storage
# =====================
STUDENTS: List[Student] = [
    Student(first_name="Alice",
            last_name="Johnson",
            age=20,
            gender=GenderEnum.female,
            email="alice.johnson@student-university.co.uk",
            phone="+1234567890"),

    Student(first_name="Bob",
            last_name="Smith",
            age=22,
            gender=GenderEnum.male,
            email="bob.smith@student-university.co.uk",
            phone="+19876543210")
]


# =====================
# Normalize phone numbers
# Keep '+' and digits only
# =====================
def normalize_phone(phone: str) -> str:
    phone = re.sub(r"[^\d+]", "", phone)
    if not phone.startswith("+"):
        phone = "+" + phone
    return phone


# =====================
# Generate unique email safely
# =====================
def generate_student_email(first_name: str,
                           last_name: str,
                           exclude_id: Optional[UUID] = None) -> str:
    first_name = first_name.lower().strip()
    last_name = last_name.lower().strip()
    base_email = f"{first_name}.{last_name}@student-university.co.uk"
    email = base_email
    counter = 1
    while any(s.email == email and s.id != exclude_id for s in STUDENTS):
        counter += 1
        email = f"{first_name}.{last_name}{counter}@student-university.co.uk"
    return email


# =====================
# Landing page
# =====================
@app.get("/")
async def landing_page():
    return {"message": "Welcome to student DBS"}


# =====================
# Get all active students
# =====================
@app.get("/students", response_model=List[Student])
async def get_all_students():
    return [s for s in STUDENTS if s.is_active]


# =====================
# Add a new student
# =====================
@app.post("/students",
          response_model=Student,
          status_code=status.HTTP_201_CREATED)
async def add_student(student: StudentCreate):
    student.phone = normalize_phone(student.phone)
    email = generate_student_email(student.first_name, student.last_name)
    new_student = Student(**student.model_dump(), email=email)
    STUDENTS.append(new_student)
    return new_student


# =====================
# Update student safely
# =====================
@app.put("/students/{student_id}",
         response_model=Student)
async def update_student(student_id: UUID, student_update: StudentUpdate):
    for student in STUDENTS:
        if student.id == student_id and student.is_active:
            update_data = student_update.model_dump(exclude_unset=True)
            if "phone" in update_data:
                update_data["phone"] = normalize_phone(update_data["phone"])
            for key, value in update_data.items():
                setattr(student, key, value)
            if update_data.get("first_name") or update_data.get("last_name"):
                student.email = generate_student_email(student.first_name,
                                                       student.last_name,
                                                       exclude_id=student.id)
            student.updated_at = datetime.now()
            return student
    raise HTTPException(status_code=404, detail="Student not found")


# =====================
# Soft delete student
# =====================
@app.delete("/students/{student_id}", response_model=Student)
async def delete_student(student_id: UUID):
    for student in STUDENTS:
        if student.id == student_id and student.is_active:
            student.is_active = False
            student.updated_at = datetime.now()
            return student
    raise HTTPException(status_code=404, detail="Student not found")


# =====================
# Search students with filters, pagination, sorting
# =====================
@app.get("/students/search", response_model=List[Student])
async def search_students(
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    gender: Optional[GenderEnum] = Query(None),
    min_age: Optional[int] = Query(None, ge=0),
    max_age: Optional[int] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: Optional[str] = Query("first_name"),
    sort_order: Optional[str] = Query("asc")
):
    results = [s for s in STUDENTS if s.is_active]

    # Filtering
    if first_name:
        results = [
            s for s in results if first_name.lower() in s.first_name.lower()
        ]
    if last_name:
        results = [
            s for s in results if last_name.lower() in s.last_name.lower()
        ]
    if email:
        results = [
            s for s in results if email.lower() in s.email.lower()
        ]
    if gender:
        results = [
            s for s in results if s.gender == gender
        ]
    if min_age is not None:
        results = [
            s for s in results if s.age >= min_age
        ]
    if max_age is not None:
        results = [
            s for s in results if s.age <= max_age
        ]

    # Sorting safely
    if sort_by in {"first_name", "last_name", "email", "age"}:
        reverse = (sort_order or "asc").lower() == "desc"

        def sort_key(s):
            val = getattr(s, sort_by)
            return val.lower() if isinstance(val, str) else val

        results.sort(key=sort_key, reverse=reverse)

    # Pagination
    paginated = results[skip: skip + limit]
    if not paginated:
        raise HTTPException(
            status_code=404, detail="No matching students found")
    return paginated


# =====================
# PROJECT NOTES
# - Soft delete via is_active
# - Emails are unique; duplicates get a number appended
# - Phone numbers normalized
# - Search supports filters, pagination, sorting
# - Update auto-refreshes email if names change
# - UUIDs used consistently
#
# exclude_unset=True
# - Only include fields that the client actually
#   sent in the request, this prevents overwriting
#   existing data with None when a field is not provided
# =====================
