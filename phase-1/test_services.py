"""
Unit tests for the Todo Console App services
"""
import unittest
from src.services import TodoService
from src.models import Task


class TestTodoService(unittest.TestCase):

    def setUp(self):
        """Set up a fresh service instance for each test."""
        self.service = TodoService()

    def test_initial_state(self):
        """Test initial state of the service."""
        self.assertEqual(self.service.task_count, 0)
        self.assertEqual(len(self.service.list_tasks()), 0)

    def test_add_task_basic(self):
        """Test adding a basic task."""
        task = self.service.add_task("Test Task")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)
        self.assertEqual(self.service.task_count, 1)

    def test_add_task_with_description(self):
        """Test adding a task with description."""
        task = self.service.add_task("Test Task", "Test Description")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertFalse(task.completed)

    def test_add_task_empty_title_raises_error(self):
        """Test that adding a task with empty title raises an error."""
        with self.assertRaises(ValueError):
            self.service.add_task("")

        with self.assertRaises(ValueError):
            self.service.add_task("   ")

        with self.assertRaises(ValueError):
            self.service.add_task(None)

    def test_add_multiple_tasks_unique_ids(self):
        """Test that multiple tasks get unique IDs."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)
        self.assertEqual(self.service.task_count, 3)

    def test_list_tasks_empty(self):
        """Test listing tasks when none exist."""
        tasks = self.service.list_tasks()

        self.assertEqual(len(tasks), 0)
        self.assertEqual(tasks, [])

    def test_list_tasks_with_items(self):
        """Test listing tasks when they exist."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")

        tasks = self.service.list_tasks()

        self.assertEqual(len(tasks), 2)
        self.assertIn(task1, tasks)
        self.assertIn(task2, tasks)

    def test_list_tasks_sorted_by_id(self):
        """Test that tasks are returned sorted by ID."""
        task3 = self.service.add_task("Task 3")  # ID 1
        task1 = self.service.add_task("Task 1")  # ID 2
        task2 = self.service.add_task("Task 2")  # ID 3

        tasks = self.service.list_tasks()

        # Check that they are sorted by ID in ascending order (1, 2, 3)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[2].id, 3)

    def test_get_task_existing(self):
        """Test getting an existing task."""
        original_task = self.service.add_task("Test Task")
        retrieved_task = self.service.get_task(original_task.id)

        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.id, original_task.id)
        self.assertEqual(retrieved_task.title, original_task.title)

    def test_get_task_nonexistent(self):
        """Test getting a non-existent task."""
        result = self.service.get_task(999)

        self.assertIsNone(result)

    def test_update_task_partial_fields(self):
        """Test updating only some fields of a task."""
        task = self.service.add_task("Original Title", "Original Description")

        # Update only the title
        updated_task = self.service.update_task(task.id, title="New Title")

        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.id, task.id)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "Original Description")  # Unchanged
        self.assertFalse(updated_task.completed)  # Unchanged

    def test_update_task_all_fields(self):
        """Test updating all fields of a task."""
        task = self.service.add_task("Original Title", "Original Description")

        updated_task = self.service.update_task(task.id, title="New Title", description="New Description")

        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.id, task.id)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "New Description")
        self.assertFalse(updated_task.completed)  # Unchanged

    def test_update_task_nonexistent(self):
        """Test updating a non-existent task."""
        result = self.service.update_task(999, title="New Title")

        self.assertIsNone(result)

    def test_update_task_empty_title_raises_error(self):
        """Test that updating with empty title raises an error."""
        task = self.service.add_task("Original Title")

        with self.assertRaises(ValueError):
            self.service.update_task(task.id, title="")

        with self.assertRaises(ValueError):
            self.service.update_task(task.id, title="   ")

    def test_delete_task_existing(self):
        """Test deleting an existing task."""
        task = self.service.add_task("Test Task")
        initial_count = self.service.task_count

        success = self.service.delete_task(task.id)

        self.assertTrue(success)
        self.assertEqual(self.service.task_count, initial_count - 1)
        self.assertIsNone(self.service.get_task(task.id))

    def test_delete_task_nonexistent(self):
        """Test deleting a non-existent task."""
        success = self.service.delete_task(999)

        self.assertFalse(success)
        self.assertEqual(self.service.task_count, 0)

    def test_toggle_completion(self):
        """Test toggling task completion status."""
        task = self.service.add_task("Test Task")

        # Initially incomplete
        self.assertFalse(task.completed)

        # Toggle to complete
        toggled_task = self.service.toggle_completion(task.id)
        self.assertTrue(toggled_task.completed)

        # Toggle back to incomplete
        toggled_task2 = self.service.toggle_completion(task.id)
        self.assertFalse(toggled_task2.completed)

    def test_toggle_completion_nonexistent(self):
        """Test toggling completion for a non-existent task."""
        result = self.service.toggle_completion(999)

        self.assertIsNone(result)

    def test_task_count_property(self):
        """Test the task_count property."""
        self.assertEqual(self.service.task_count, 0)

        self.service.add_task("Task 1")
        self.assertEqual(self.service.task_count, 1)

        self.service.add_task("Task 2")
        self.assertEqual(self.service.task_count, 2)

        self.service.delete_task(1)
        self.assertEqual(self.service.task_count, 1)


if __name__ == '__main__':
    unittest.main()