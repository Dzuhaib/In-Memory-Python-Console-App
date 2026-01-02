# Quickstart: In-Memory Todo List Application

This guide explains how to run the console-based to-do list application.

## Prerequisites

-   Python 3.11 or higher.

## Running the Application

1.  Navigate to the `src/todo_app` directory in your terminal.
2.  Run the application using the following command:

    ```bash
    python main.py
    ```

3.  The application will start and display a menu of options.

## How to Use

The application will present a menu with the following options:

1.  **Add a new task**: Prompts you to enter a description for the new task.
2.  **View all tasks**: Displays all current tasks with their ID and completion status.
3.  **Mark a task as complete**: Prompts you to enter the ID of the task you want to mark as complete.
4.  **Clear completed tasks**: Removes all completed tasks from the list.
5.  **Exit**: Quits the application.

Follow the on-screen prompts to manage your to-do list. Since the application is in-memory, all tasks will be lost when you exit.
