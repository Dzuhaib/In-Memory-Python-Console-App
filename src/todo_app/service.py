from src.todo_app.models import Task
from dataclasses import dataclass

class TodoService:
    def __init__(self):
        self.tasks: list[Task] = []
        self.next_id = 1

    def add_task(self, description: str):
        if not description:
            raise ValueError("Task description cannot be empty.")
        task = Task(id=self.next_id, description=description)
        self.tasks.append(task)
        self.next_id += 1

    def view_tasks(self) -> list[Task]:
        return self.tasks
    
    def complete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                return True
    def clear_completed_tasks(self):
        self.tasks = [task for task in self.tasks if not task.completed]