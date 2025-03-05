from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: Optional[str]
    title: str
    description: Optional[str]
    completed: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }