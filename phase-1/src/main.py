from .services import TodoService


def menu():
    print("\nTodo App")
    print("1. Add Todo")
    print("2. List Todos")
    print("3. Complete Todo")
    print("4. Exit")


def main():
    service = TodoService()

    while True:
        menu()
        choice = input("Choose: ")

        if choice == "1":
            title = input("Enter todo: ")
            service.add_todo(title)

        elif choice == "2":
            service.list_todos()

        elif choice == "3":
            num = int(input("Todo number: ")) - 1
            service.complete_todo(num)

        elif choice == "4":
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
