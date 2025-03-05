from abc import ABC, abstractmethod
from typing import List
from domain.task import Task


class TaskRepository(ABC):
    @abstractmethod
    async def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    async def get_by_id(self, task_id: str) -> Task:
        pass

    @abstractmethod
    async def update(self, task_id: str, task: Task) -> Task:
        pass

    @abstractmethod
    async def delete(self, task_id: str) -> None:
        pass
