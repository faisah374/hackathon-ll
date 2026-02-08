"""
Integration tests for the Todo Console App
Tests the integration between models, services, and CLI
"""
import unittest
import io
import sys
from contextlib import redirect_stdout
from src.services import TodoService
from src.cli import TodoCLI


class TestTodoAppIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a fresh service and CLI instance for each test."""
        self.service = TodoService()
        self.cli = TodoCLI(self.service)

    def test_full_workflow_add_list_update_delete(self):
        """Test the complete workflow: add, list, update, delete."""
        # Add tasks
        args_add1 = ['add', 'Buy groceries', '-d', 'Milk, bread, eggs']
        args_add2 = ['add', 'Walk the dog']

        # Capture output for add commands
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(args_add1)
        output_add1 = f.getvalue()

        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(args_add2)
        output_add2 = f.getvalue()

        # Verify tasks were added
        self.assertIn('Added task:', output_add1)
        self.assertIn('Buy groceries', output_add1)
        self.assertIn('Added task:', output_add2)
        self.assertIn('Walk the dog', output_add2)

        # Verify task count
        self.assertEqual(self.service.task_count, 2)

        # List tasks
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['list'])
        output_list = f.getvalue()

        # Verify both tasks appear in list
        self.assertIn('Total tasks: 2', output_list)
        self.assertIn('Buy groceries', output_list)
        self.assertIn('Walk the dog', output_list)

        # Update a task
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['update', '1', '-t', 'Buy food'])
        output_update = f.getvalue()

        # Verify task was updated
        self.assertIn('Updated task:', output_update)
        self.assertIn('Buy food', output_update)

        # Verify update worked by listing again
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['list'])
        output_list_after_update = f.getvalue()

        self.assertIn('Buy food', output_list_after_update)  # Changed title
        self.assertNotIn('Buy groceries', output_list_after_update)  # Old title gone

        # Delete a task
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['delete', '1'])
        output_delete = f.getvalue()

        # Verify deletion
        self.assertIn('Deleted task with ID 1', output_delete)
        self.assertEqual(self.service.task_count, 1)

        # List again to confirm only one task remains
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['list'])
        output_final_list = f.getvalue()

        self.assertIn('Total tasks: 1', output_final_list)
        self.assertNotIn('Buy food', output_final_list)  # Deleted task gone

    def test_toggle_completion(self):
        """Test toggling task completion works through CLI."""
        # Add a task
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['add', 'Complete this task'])
        f.seek(0)  # Reset buffer

        # Toggle completion
        with redirect_stdout(f):
            self.cli.run_command(['toggle', '1'])
        output_toggle = f.getvalue()

        # Verify toggle worked
        self.assertIn('Toggled task:', output_toggle)
        self.assertIn('[x]', output_toggle)  # Should show completed

        # Verify state changed by listing
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['list'])
        output_list = f.getvalue()

        self.assertIn('[x]', output_list)  # Should show completed

        # Toggle again to incomplete
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['toggle', '1'])
        output_toggle2 = f.getvalue()

        self.assertIn('Toggled task:', output_toggle2)
        self.assertIn('[ ]', output_toggle2)  # Should show incomplete

    def test_error_handling_invalid_commands(self):
        """Test error handling for invalid operations."""
        # Try to update non-existent task
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['update', '999', '-t', 'New Title'])
        output = f.getvalue()

        self.assertIn('Error: Task with ID 999 not found', output)

        # Try to delete non-existent task
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['delete', '999'])
        output = f.getvalue()

        self.assertIn('Error: Task with ID 999 not found', output)

        # Try to toggle non-existent task
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['toggle', '999'])
        output = f.getvalue()

        self.assertIn('Error: Task with ID 999 not found', output)

    def test_list_empty_tasks(self):
        """Test listing when no tasks exist."""
        f = io.StringIO()
        with redirect_stdout(f):
            self.cli.run_command(['list'])
        output = f.getvalue()

        self.assertIn('No tasks found.', output)

    def test_add_empty_title_error(self):
        """Test that adding task with empty title shows error."""
        # Test this by trying to add a task with empty title via the service
        with self.assertRaises(ValueError):
            self.service.add_task('')


if __name__ == '__main__':
    unittest.main()