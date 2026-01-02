import unittest
from src.todo_app.models import Task
from src.todo_app.service import TodoService

class TestTodoService(unittest.TestCase):

    def setUp(self):
        # Reset the service for each test to ensure isolation
        self.service = TodoService()

    def test_add_task_single_item(self):
        self.service.add_task("Buy milk")
        tasks = self.service.view_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Buy milk")
        self.assertEqual(tasks[0].id, 1)
        self.assertFalse(tasks[0].completed)

    def test_add_task_multiple_items(self):
        self.service.add_task("Buy milk")
        self.service.add_task("Walk the dog")
        tasks = self.service.view_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[1].description, "Walk the dog")

    def test_view_tasks_with_multiple_items(self):
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        tasks = self.service.view_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].description, "Task 1")
        self.assertEqual(tasks[1].description, "Task 2")

    def test_view_tasks_with_no_items(self):
        tasks = self.service.view_tasks()
        self.assertEqual(len(tasks), 0)
        self.assertEqual(tasks, [])

    def test_complete_task_existing_id(self):
        self.service.add_task("Task to complete")
        self.service.complete_task(1)
        tasks = self.service.view_tasks()
        self.assertTrue(tasks[0].completed)

    def test_complete_task_non_existent_id(self):
        self.service.add_task("Task 1")
        result = self.service.complete_task(999) # Non-existent ID
        self.assertFalse(result)
        tasks = self.service.view_tasks()
        self.assertFalse(tasks[0].completed) # Ensure existing tasks are not completed

    def test_clear_completed_tasks_removes_only_completed(self):
        self.service.add_task("Task 1 (uncompleted)")
        self.service.add_task("Task 2 (completed)")
        self.service.add_task("Task 3 (uncompleted)")
        self.service.complete_task(2) # Complete Task 2

        self.service.clear_completed_tasks()

        tasks = self.service.view_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].description, "Task 1 (uncompleted)")
        self.assertFalse(tasks[0].completed)
        self.assertEqual(tasks[1].description, "Task 3 (uncompleted)")
        self.assertFalse(tasks[1].completed)

    def test_clear_completed_tasks_no_completed_items(self):
        self.service.add_task("Task 1 (uncompleted)")
        self.service.add_task("Task 2 (uncompleted)")

        self.service.clear_completed_tasks()

        tasks = self.service.view_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].description, "Task 1 (uncompleted)")
        self.assertFalse(tasks[0].completed)
        self.assertEqual(tasks[1].description, "Task 2 (uncompleted)")
        self.assertFalse(tasks[1].completed)

if __name__ == '__main__':
    unittest.main()