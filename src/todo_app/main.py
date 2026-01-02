import sys
import os

# Add the project root to the sys.path to enable correct module imports
# when running main.py directly from its subdirectory.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.todo_app.service import TodoService

def print_menu():
    print("\n--- To-Do Application ---")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Clear completed tasks")
    print("5. Exit")
    print("-------------------------")

if __name__ == "__main__":
    service = TodoService()
    
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1': # Add a new task
            description = input("Enter task description: ")
            try:
                service.add_task(description)
                print("Task added successfully!")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2': # View all tasks
            tasks = service.view_tasks()
            if not tasks:
                print("Your to-do list is empty!")
            else:
                print("\n--- Your To-Do List ---")
                for task in tasks:
                    status = "[Completed]" if task.completed else "[Incomplete]"
                    print(f"{status} {task.id}. {task.description}")
                print("-------------------------")
        
        elif choice == '3': # Mark a task as complete
            try:
                task_id = int(input("Enter the ID of the task to complete: "))
                if service.complete_task(task_id):
                    print(f"Task {task_id} marked as complete!")
                else:
                    print(f"Error: Task with ID {task_id} not found.")
            except ValueError:
                print("Error: Invalid input. Please enter a number for the Task ID.")
        
        elif choice == '4': # Clear completed tasks
            initial_task_count = len(service.view_tasks())
            service.clear_completed_tasks()
            final_task_count = len(service.view_tasks())
            if initial_task_count > final_task_count:
                print("Completed tasks cleared!")
            else:
                print("No completed tasks to clear.")
        
        elif choice == '5': # Exit
            print("Exiting To-Do Application. Goodbye!")
            break
        
        else: # Invalid choice
            print("Invalid choice. Please enter a number between 1 and 5.")