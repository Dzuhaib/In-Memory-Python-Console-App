"""Main entry point for the todo CLI application."""

import sys

from src.services.task_service import TaskService
from src.cli.commands import CommandHandler


def main() -> None:
    """Run the todo CLI application."""
    service = TaskService()
    handler = CommandHandler(service)

    print("Todo App v1.0.0")
    print('Type "help" for available commands.')
    print()

    while True:
        try:
            user_input = input("todo> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        result = handler.execute(user_input)

        if result is None:
            print("Goodbye!")
            break

        if result:
            print(result)


if __name__ == "__main__":
    main()
