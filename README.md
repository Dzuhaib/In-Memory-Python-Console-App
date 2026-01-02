# In-Memory Python Console Todo List Application

## Project Description
This is a simple console-based To-Do List application implemented in Python. It allows users to manage their daily tasks directly from the terminal. As an in-memory application, all tasks are stored temporarily and are lost once the application is closed. This project serves as Phase 1 of the "Evolution of Todo" series, focusing on core functionality and adherence to strict development principles, including the exclusive use of Python's standard library.

## Features
-   **Add Task**: Add new tasks to your to-do list with a description.
-   **View Tasks**: Display all current tasks, showing their unique ID, description, and completion status.
-   **Mark Task as Complete**: Change the status of a task from pending to complete using its ID.
-   **Clear Completed Tasks**: Remove all tasks that have been marked as complete from the list.
-   **In-Memory Storage**: All data is stored in RAM and is not persisted.
-   **Console Interface**: Fully interactive via command-line input.

## How to Run

### Prerequisites
-   Python 3.11 or higher installed on your system.

### Running from Project Root

1.  Navigate to the root directory of the project in your terminal.
    ```bash
    cd /path/to/your/project/root
    ```
2.  Run the application using the following command:
    ```bash
    python -m src.todo_app.main
    ```

### Running from Application Directory (src/todo_app)

1.  Navigate to the application's directory in your terminal.
    ```bash
    cd /path/to/your/project/root/src/todo_app
    ```
2.  Run the application using the following command:
    ```bash
    python main.py
    ```
    *(Note: The application's `main.py` has been modified to support this direct execution by adjusting Python's import paths.)*

## Example Usage

Once the application is running, you will be presented with a menu:

```
--- To-Do Application ---
1. Add a new task
2. View all tasks
3. Mark a task as complete
4. Clear completed tasks
5. Exit
-------------------------
Enter your choice: 
```

Follow the on-screen prompts to manage your tasks. For example:
-   Enter `1` to add a task, then type your task description.
-   Enter `2` to see your current list of tasks.
-   Enter `3` to mark a task complete by its ID.
-   Enter `4` to remove completed tasks.
-   Enter `5` to exit the application.

## Technology Used
-   Python (3.11+)
-   Python Standard Library (no external dependencies)

## Future Enhancements
This being Phase 1, the application currently operates entirely in memory. Future phases may introduce persistence, more advanced task management features, and potentially a graphical user interface.
