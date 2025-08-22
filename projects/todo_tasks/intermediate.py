from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional, List
import uuid

# create FastAPI app
app = FastAPI()


# ========== Enums for restricted choices
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    complete = "complete"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCategory(str, Enum):
    work = "work"
    personal = "personal"
    urgent = "urgent"
    other = "other"


# ========== Task model
class TodoTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_name: str
    task_description: str
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.low
    due_date: Optional[datetime] = None
    category: Optional[TaskCategory] = TaskCategory.other
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ========== In-memory storage
todo_tasks: List[TodoTask] = []


# ========== Routes
# ========== Welcome message
@app.get("/")
async def main():
    # return a welcome message
    return {"message": "Welcome to Task API App."}


# ========== Return all tasks
@app.get("/tasks/", response_model=List[TodoTask])
async def get_all_tasks():
    # return the list of all tasks
    return todo_tasks


# ========== Add new task
@app.post("/tasks/", response_model=TodoTask)
async def add_task(task: TodoTask):
    # ensure id is generated if missing
    if not task.id:
        task.id = str(uuid.uuid4())
    # set the updated_at timestamp to now
    task.updated_at = datetime.now()
    # add the task to the in-memory list
    todo_tasks.append(task)
    return task


# ========== Edit existing task
@app.put("/tasks/{task_id}", response_model=TodoTask)
async def edit_task(task_id: str, updated_task: TodoTask):
    # loop through all tasks with index to locate the one to update
    for index, task in enumerate(todo_tasks):
        # check if the current task's ID matches the ID from the URL
        if task.id == task_id:
            # preserve the original task's ID
            updated_task.id = task.id
            # preserve the original created_at timestamp
            updated_task.created_at = task.created_at
            # update the updated_at timestamp to the current time
            updated_task.updated_at = datetime.now()
            # replace the old task in the list with the updated task
            todo_tasks[index] = updated_task
            # return the updated task as the response
            return updated_task
    # if no task matches the given ID, raise a 404 Not Found error
    raise HTTPException(status_code=404, detail="Task not found")


# ==========  Delete existing task
@app.delete("/tasks/{task_id}", response_model=TodoTask)
async def delete_task(task_id: str):
    # loop through all tasks in the in-memory list
    for task in todo_tasks:
        # check if the current task's ID matches the one provided in the URL
        if task.id == task_id:
            # if found, remove the task from the list
            todo_tasks.remove(task)
            # Return the deleted task as the response
            return task
    # if no task matches the given ID, raise a 404 Not Found error
    raise HTTPException(status_code=404, detail="Task not found")
