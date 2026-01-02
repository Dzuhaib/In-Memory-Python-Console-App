# Phase I: In-Memory Python Console Todo App - Constitution and Specification

## Constitution

### 1. Project Overview
This document outlines the constitution and specifications for Phase I of the "Evolution of Todo" project. Phase I focuses on developing a foundational Todo list application as an in-memory Python console application. This phase establishes the core functionalities required for managing a basic list of tasks.

### 2. Guiding Principles
*   **Simplicity:** The application should be straightforward to use and understand from a console interface perspective.
*   **In-Memory Data:** All task data will reside in memory and will not persist across application runs.
*   **Console-Based Interaction:** User interaction will be exclusively through the command-line interface.
*   **Core Functionality First:** Focus on implementing the essential task management features as defined in the project brief.
*   **Pythonic Design:** Adhere to Python best practices and idioms.

### 3. High-Level Architecture
The application will consist of:
*   A main entry point for running the console application.
*   A data structure (e.g., a list of dictionaries or objects) to hold todo items in memory.
*   Functions or methods to perform CRUD (Create, Read, Update, Delete) operations on the todo items.
*   A command-line interface (CLI) to allow users to interact with these functions.

## Specification

### 1. Todo Item Structure
Each todo item will be represented by:
*   **ID:** A unique integer identifier, automatically assigned.
*   **Description:** A string describing the task.
*   **Completed:** A boolean indicating if the task is completed (default: `False`).

### 2. Core Features

#### 2.1. Add Task
*   **Description:** Allows the user to create a new todo item.
*   **Input:** Task description (string).
*   **Process:**
    1.  Prompts the user for a task description.
    2.  Creates a new todo item with a unique ID, the provided description, and `Completed` status set to `False`.
    3.  Adds the new item to the in-memory list.
*   **Output:** Confirmation message that the task was added, along with its ID and description.

#### 2.2. View Task List
*   **Description:** Displays all existing todo items.
*   **Input:** None.
*   **Process:**
    1.  Iterates through the in-memory list of todo items.
    2.  Presents each item with its ID, description, and completion status.
    3.  If the list is empty, displays a message indicating no tasks.
*   **Output:** A formatted list of all tasks, showing `[ID] [Status] Description` (e.g., `[1] [ ] Buy groceries`, `[2] [x] Finish report`).

#### 2.3. Update Task
*   **Description:** Allows the user to modify the description of an existing todo item.
*   **Input:** Task ID (integer), New Description (string).
*   **Process:**
    1.  Prompts the user for the ID of the task to update.
    2.  Prompts for the new description.
    3.  Finds the task by ID.
    4.  If found, updates its description.
    5.  If not found, displays an error message.
*   **Output:** Confirmation message if updated, or error message if task not found.

#### 2.4. Mark as Complete
*   **Description:** Toggles the completion status of a todo item.
*   **Input:** Task ID (integer).
*   **Process:**
    1.  Prompts the user for the ID of the task to mark/unmark.
    2.  Finds the task by ID.
    3.  If found, toggles its `Completed` status.
    4.  If not found, displays an error message.
*   **Output:** Confirmation message with the new status, or error message if task not found.

#### 2.5. Delete Task
*   **Description:** Removes an existing todo item from the list.
*   **Input:** Task ID (integer).
*   **Process:**
    1.  Prompts the user for the ID of the task to delete.
    2.  Finds the task by ID.
    3.  If found, removes it from the in-memory list.
    4.  If not found, displays an error message.
*   **Output:** Confirmation message if deleted, or error message if task not found.
