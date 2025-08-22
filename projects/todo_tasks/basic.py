from fastapi import FastAPI
# from pydantic import BaseModel

"""
HTTP Methods:
* GET -> get information
* POST -> create/submit to the server
* PUT -> edit an existing information
* DELETE -> delete an existing information
"""
app = FastAPI()

# list of tasks stored as dictionaries
todo_tasks = [
    {"task_id": 1, "task_name": "shopping",
        "task_description": "purchase items from shopping list"},
    {"task_id": 2, "task_name": "medicine",
     "task_description": "collect medicine from pharmacy"},
    {"task_id": 3, "task_name": "exam",
     "task_description": "study for exam"},
    {"task_id": 4, "task_name": "meditate",
     "task_description": "meditate for self-development"},
    {"task_id": 5, "task_name": "chores",
     "task_description": "complete house chores mentioned on list"}
]


# =============== get all tasks
@app.get("/")
async def get_all_tasks():
    return todo_tasks


# define an endpoint that takes a task_id from the URL
@app.get("/tasks/{task_id}")
# FastAPI makes sure task_id is an integer
async def get_task(task_id: int):
    # loop through each dictionary in the todo_tasks list
    for task in todo_tasks:
        # check if the current task_id matches the one from the URL
        if task["task_id"] == task_id:
            # if it matches, return that task as JSON
            return {"result": task}


# =============== add new task
@app.post("/tasks/")
async def post_task(new_task: dict):
    todo_tasks.append(new_task)
    return {"message": "task added", "task": new_task}


# =============== edit existing task
@app.put("/tasks/{task_id}")
async def edit_task(task_id: int, updated_task: dict):
    # loop through all tasks in the todo_tasks list
    for task in todo_tasks:
        # check if the current task's id matches the one from the url
        if task["task_id"] == task_id:
            # update existing task dictionary with new values from request body
            task.update(updated_task)
            # return a success message along with the updated task
            return {"message": "task updated", "task": task}
    # if no task with the given id is found, return an error message
    return {"message": "task not found"}


# =============== delete existing task
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    # loop through all tasks
    for task in todo_tasks:
        # check if ids match
        if task["task_id"] == task_id:
            # remove the task from the list
            todo_tasks.remove(task)
            return {"message": "task deleted", "task": task}
