from .models import Todo


class TodoService:
    def __init__(self):
        self.todos = []

    def add_todo(self, title):
        todo = Todo(title)
        self.todos.append(todo)

    def list_todos(self):
        if not self.todos:
            print("No todos yet.")
            return

        for i, todo in enumerate(self.todos, 1):
            print(f"{i}. {todo}")

    def complete_todo(self, index):
        if 0 <= index < len(self.todos):
            self.todos[index].mark_done()
        else:
            print("Invalid number!")
