"""Task service - business logic for task operations."""

from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from models.task import Priority, Task
from utils.logger import get_logger

logger = get_logger(__name__)


class TaskService:
    """Service class for task CRUD and query operations."""

    def __init__(self, session: Session):
        """Initialize with database session.

        Args:
            session: SQLModel database session
        """
        self.session = session

    def create_task(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None,
    ) -> Task:
        """Create a new task.

        Args:
            title: Task description
            priority: Priority level (default: MEDIUM)
            tags: List of tags (default: empty)

        Returns:
            The created Task instance
        """
        task = Task(
            title=title,
            priority=priority,
            tags=tags or [],
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        logger.info(f"Created task #{task.id}: {task.title}")
        return task

    def list_tasks(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None,
        sort_by: Optional[str] = "id",
    ) -> List[Task]:
        """List all tasks with optional filtering and sorting.

        Args:
            search: Case-insensitive search term for titles
            status: Filter by 'complete' or 'incomplete'
            priority: Filter by priority level
            tag: Filter by tag
            sort_by: Sort order ('priority', 'alpha', or 'id')

        Returns:
            List of matching tasks
        """
        statement = select(Task)

        # Apply search filter
        if search:
            statement = statement.where(Task.title.ilike(f"%{search}%"))

        # Apply status filter
        if status == "complete":
            statement = statement.where(Task.completed == True)
        elif status == "incomplete":
            statement = statement.where(Task.completed == False)

        # Apply priority filter
        if priority:
            statement = statement.where(Task.priority == priority)

        tasks = list(self.session.exec(statement).all())

        # Apply tag filter (done in Python since JSON querying varies by DB)
        if tag:
            tasks = [t for t in tasks if tag in t.tags]

        # Apply sorting
        tasks = self.sort_tasks(tasks, sort_by)

        logger.debug(f"Listed {len(tasks)} tasks")
        return tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task if found, None otherwise
        """
        return self.session.get(Task, task_id)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        priority: Optional[Priority] = None,
    ) -> Optional[Task]:
        """Update a task's title and/or priority.

        Args:
            task_id: Task identifier
            title: New title (if provided)
            priority: New priority (if provided)

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.session.get(Task, task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if priority is not None:
            task.priority = priority

        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        logger.info(f"Updated task #{task_id}")
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: Task identifier

        Returns:
            True if deleted, False if not found
        """
        task = self.session.get(Task, task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        logger.info(f"Deleted task #{task_id}")
        return True

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle the completion status of a task.

        Args:
            task_id: Task identifier

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.session.get(Task, task_id)
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        logger.info(f"Toggled task #{task_id} completion to {task.completed}")
        return task

    def add_tag(self, task_id: int, tag: str) -> Optional[Task]:
        """Add a tag to a task.

        Args:
            task_id: Task identifier
            tag: Tag to add

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.session.get(Task, task_id)
        if not task:
            return None

        if tag not in task.tags:
            task.tags = task.tags + [tag]  # Create new list to trigger update
            task.updated_at = datetime.utcnow()
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
            logger.info(f"Added tag '{tag}' to task #{task_id}")
        return task

    def remove_tag(self, task_id: int, tag: str) -> Optional[Task]:
        """Remove a tag from a task.

        Args:
            task_id: Task identifier
            tag: Tag to remove

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.session.get(Task, task_id)
        if not task:
            return None

        if tag in task.tags:
            task.tags = [t for t in task.tags if t != tag]
            task.updated_at = datetime.utcnow()
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
            logger.info(f"Removed tag '{tag}' from task #{task_id}")
        return task

    def sort_tasks(self, tasks: List[Task], sort_by: Optional[str] = "id") -> List[Task]:
        """Sort a list of tasks.

        Args:
            tasks: List of tasks to sort
            sort_by: Sort order ('priority', 'alpha', or 'id')

        Returns:
            Sorted list of tasks
        """
        if sort_by == "priority":
            priority_order = {Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
            return sorted(tasks, key=lambda t: priority_order.get(t.priority, 2))
        elif sort_by == "alpha":
            return sorted(tasks, key=lambda t: t.title.lower())
        else:  # Default to 'id'
            return sorted(tasks, key=lambda t: t.id or 0)
