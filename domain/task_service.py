from typing import List
from domain.task import Task
from ports.task_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task: Task) -> Task:
        return await self.repository.create(task)

    async def get_tasks(self) -> List[Task]:
        return await self.repository.get_all()

    async def get_task(self, task_id: str) -> Task:
        task = await self.repository.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task

    async def update_task(self, task_id: str, task: Task) -> Task:
        existing_task = await self.repository.get_by_id(task_id)
        if not existing_task:
            raise ValueError(f"Task {task_id} not found")
        return await self.repository.update(task_id, task)

    async def delete_task(self, task_id: str) -> None:
        existing_task = await self.repository.get_by_id(task_id)
        if not existing_task:
            raise ValueError(f"Task {task_id} not found")
        await self.repository.delete(task_id)
