# adapters/http_controller.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from domain.task import Task
from domain.task_service import TaskService
from adapters.firestore_repository import FirestoreTaskRepository
from config.auth import get_current_user, authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="Backend para tasks")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://womfrontend.web.app"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
task_service = TaskService(FirestoreTaskRepository())


class TaskDTO(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskDTOI(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


@app.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/tasks/", response_model=TaskDTO, status_code=201)
async def create_task(task_dto: TaskDTOI, user: str = Depends(get_current_user)):
    task = Task(id=None, **task_dto.dict())
    created_task = await task_service.create_task(task)
    return created_task


@app.get("/tasks/", response_model=List[TaskDTO])
async def get_tasks(user: str = Depends(get_current_user)):
    tasks = await task_service.get_tasks()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskDTO)
async def get_task(task_id: str, user: str = Depends(get_current_user)):
    try:
        task = await task_service.get_task(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/tasks/{task_id}", response_model=TaskDTO)
async def update_task(task_id: str, task_dto: TaskDTOI, user: str = Depends(get_current_user)):
    try:
        task = Task(id=task_id, **task_dto.dict())
        updated_task = await task_service.update_task(task_id, task)
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, user: str = Depends(get_current_user)):
    try:
        await task_service.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
