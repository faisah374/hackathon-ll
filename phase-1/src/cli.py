"""
Command-line interface for the Todo Console App.
Handles user input, command parsing, and output formatting.
"""
import argparse
from typing import List, Optional
from .models import Task
from .services import TodoService


class TodoCLI:
    """
    Command-line interface for the Todo application.
    Maps user commands to service operations and formats output.
    """

    def __init__(self, service: TodoService):
        """Initialize CLI with a TodoService instance."""
        self.service = service
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="Todo Console Application",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s add "Buy groceries" -d "Milk, bread, eggs"
  %(prog)s list
  %(prog)s update 1 -t "Buy food" -d "Milk, bread, eggs, cheese"
  %(prog)s delete 1
  %(prog)s toggle 1
            """.strip()
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('title', help='Task title')
        add_parser.add_argument('-d', '--description', help='Task description')

        # List command
        list_parser = subparsers.add_parser('list', help='List all tasks')

        # Update command
        update_parser = subparsers.add_parser('update', help='Update a task')
        update_parser.add_argument('id', type=int, help='Task ID')
        update_parser.add_argument('-t', '--title', help='New title')
        update_parser.add_argument('-d', '--description', help='New description')

        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('id', type=int, help='Task ID')

        # Toggle command
        toggle_parser = subparsers.add_parser('toggle', help='Toggle task completion')
        toggle_parser.add_argument('id', type=int, help='Task ID')

        return parser

    def run_command(self, args: Optional[List[str]] = None) -> bool:
        """
        Parse arguments and execute the appropriate command.

        Args:
            args: Command line arguments (defaults to sys.argv)

        Returns:
            True if command executed successfully, False otherwise
        """
        parsed_args = self.parser.parse_args(args)

        if not parsed_args.command:
            self.parser.print_help()
            return False

        try:
            if parsed_args.command == 'add':
                self._handle_add(parsed_args)
            elif parsed_args.command == 'list':
                self._handle_list()
            elif parsed_args.command == 'update':
                self._handle_update(parsed_args)
            elif parsed_args.command == 'delete':
                self._handle_delete(parsed_args)
            elif parsed_args.command == 'toggle':
                self._handle_toggle(parsed_args)
            else:
                self.parser.print_help()
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

        return True

    def _handle_add(self, args) -> None:
        """Handle the add command."""
        try:
            task = self.service.add_task(args.title, args.description)
            print(f"Added task: {task.detailed_str()}")
        except ValueError as e:
            print(f"Error adding task: {e}")

    def _handle_list(self) -> None:
        """Handle the list command."""
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks found.")
        else:
            print(f"Total tasks: {len(tasks)}")
            for task in tasks:
                print(task.detailed_str())

    def _handle_update(self, args) -> None:
        """Handle the update command."""
        task = self.service.update_task(args.id, args.title, args.description)

        if task is None:
            print(f"Error: Task with ID {args.id} not found")
        else:
            print(f"Updated task: {task.detailed_str()}")

    def _handle_delete(self, args) -> None:
        """Handle the delete command."""
        success = self.service.delete_task(args.id)

        if success:
            print(f"Deleted task with ID {args.id}")
        else:
            print(f"Error: Task with ID {args.id} not found")

    def _handle_toggle(self, args) -> None:
        """Handle the toggle command."""
        task = self.service.toggle_completion(args.id)

        if task is None:
            print(f"Error: Task with ID {args.id} not found")
        else:
            status = "completed" if task.completed else "incomplete"
            print(f"Toggled task: {task} ({status})")

    def run_interactive(self) -> None:
        """Run the CLI in interactive mode."""
        print("Todo Console App - Interactive Mode")
        print("Type 'help' for available commands, 'quit' to exit")

        while True:
            try:
                user_input = input("\ntodo> ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self.parser.print_help()
                    continue
                elif not user_input:
                    continue

                # Split the input into arguments and run
                args = user_input.split()
                self.run_command(args)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break