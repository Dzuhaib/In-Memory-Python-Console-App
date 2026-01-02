import unittest
from dataclasses import is_dataclass
# This will fail initially because the model doesn't exist yet
from src.todo_app.models import Task

class TestTaskModel(unittest.TestCase):

    def test_task_is_dataclass(self):
        self.assertTrue(is_dataclass(Task))

    def test_create_task(self):
        task = Task(id=1, description="Buy milk")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Buy milk")
        self.assertFalse(task.completed)

if __name__ == '__main__':
    unittest.main()
