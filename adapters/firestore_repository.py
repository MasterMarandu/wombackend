from google.cloud import firestore
from domain.task import Task
from ports.task_repository import TaskRepository

class FirestoreTaskRepository(TaskRepository):
    def __init__(self):
        self.db = firestore.AsyncClient()
        self.collection = self.db.collection("tasks")

    async def create(self, task: Task) -> Task:
        doc_ref = self.collection.document()
        task.id = doc_ref.id
        await doc_ref.set(task.to_dict())
        return task

    async def get_all(self) -> list[Task]:
        docs = self.collection.stream()
        tasks = [Task(**doc.to_dict()) async for doc in docs]
        return tasks

    async def get_by_id(self, task_id: str) -> Task:
        doc = await self.collection.document(task_id).get()
        if not doc.exists:
            return None
        return Task(**doc.to_dict())

    async def update(self, task_id: str, task: Task) -> Task:
        task.id = task_id
        await self.collection.document(task_id).set(task.to_dict())
        return task

    async def delete(self, task_id: str) -> None:
        await self.collection.document(task_id).delete()