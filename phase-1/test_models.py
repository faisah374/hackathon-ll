"""
Unit tests for the Todo Console App models
"""
import unittest
from src.models import Task


class TestTask(unittest.TestCase):

    def test_create_task_valid(self):
        """Test creating a valid task with all fields."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertFalse(task.completed)

    def test_create_task_defaults(self):
        """Test creating a task with minimal fields."""
        task = Task(id=1, title="Test Task")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)

    def test_create_task_empty_title_raises_error(self):
        """Test that creating a task with empty title raises an error."""
        with self.assertRaises(ValueError):
            Task(id=1, title="")

        with self.assertRaises(ValueError):
            Task(id=1, title="   ")

        with self.assertRaises(ValueError):
            Task(id=1, title=None)

    def test_task_str_representation(self):
        """Test string representation of task."""
        task_incomplete = Task(id=1, title="Test Task", completed=False)
        task_complete = Task(id=1, title="Test Task", completed=True)

        self.assertEqual(str(task_incomplete), "[ ] 1. Test Task")
        self.assertEqual(str(task_complete), "[x] 1. Test Task")

    def test_task_detailed_str_with_description(self):
        """Test detailed string representation with description."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=True)
        expected = "[x] 1. Test Task\n    Description: Test Description"

        self.assertEqual(task.detailed_str(), expected)

    def test_task_detailed_str_without_description(self):
        """Test detailed string representation without description."""
        task = Task(id=1, title="Test Task", completed=False)
        expected = "[ ] 1. Test Task"

        self.assertEqual(task.detailed_str(), expected)


if __name__ == '__main__':
    unittest.main()