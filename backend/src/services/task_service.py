"""Task service - business logic for task operations."""

# Task T013: Update TaskService.create_task() to accept and persist due_at and remind_at
# Task T014: Update TaskService.update_task() to accept and persist due_at and remind_at
# Task T024: Add calculate_next_due_date() helper function
# Task T025: Update toggle_complete() to call recurrence spawning logic
# Task T026: Implement spawn_recurring_instance()
# Task T041: Hook EventPublisher.publish() into create_task() to publish task.created
# Task T042: Hook EventPublisher.publish() into update_task() to publish task.updated
# Task T043: Hook EventPublisher.publish() into toggle_complete() to publish task.completed
# Task T044: Hook EventPublisher.publish() into delete_task() to publish task.deleted
# Task T060: Hook schedule_reminder() into task create/update when remind_at is set
# Task T061: Hook cancel_reminder() into task delete and task complete

from datetime import datetime, timedelta
from typing import List, Optional
from dateutil.relativedelta import relativedelta

from sqlmodel import Session, select

from models.task import Priority, Task, RecurrenceRule
from utils.logger import get_logger

logger = get_logger(__name__)


class TaskService:
    """Service class for task CRUD and query operations."""

    def __init__(self, session: Session, event_publisher=None):
        """Initialize with database session and optional event publisher.

        Args:
            session: SQLModel database session
            event_publisher: Optional EventPublisher instance for publishing events
        """
        self.session = session
        self.event_publisher = event_publisher

    def create_task(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None,
        due_at: Optional[datetime] = None,
        remind_at: Optional[datetime] = None,
        recurrence_rule: Optional[RecurrenceRule] = None,
        recurrence_interval: Optional[int] = None,
    ) -> Task:
        """Create a new task.

        Task T013: Accept and persist due_at and remind_at.
        Task T041: Publish task.created event after task creation.

        Args:
            title: Task description
            priority: Priority level (default: MEDIUM)
            tags: List of tags (default: empty)
            due_at: Optional due date
            remind_at: Optional reminder time
            recurrence_rule: Optional recurrence pattern
            recurrence_interval: Optional custom interval

        Returns:
            The created Task instance
        """
        task = Task(
            title=title,
            priority=priority,
            tags=tags or [],
            due_at=due_at,
            remind_at=remind_at,
            recurrence_rule=recurrence_rule,
            recurrence_interval=recurrence_interval,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        logger.info(f"Created task #{task.id}: {task.title}")

        # T041: Publish task.created event to task-events and task-updates topics
        if self.event_publisher:
            from api.tasks import task_to_dict
            task_snapshot = task_to_dict(task)
            self.event_publisher.publish_sync("task-events", "task.created", task.id, task_snapshot, actor="user")
            self.event_publisher.publish_sync("task-updates", "task.created", task.id, task_snapshot, actor="user")

        # T060: Schedule reminder if remind_at is set
        if remind_at:
            from services.event_publisher import schedule_reminder_sync
            from config import settings
            schedule_reminder_sync(
                task_id=task.id,
                remind_at=remind_at,
                payload={"title": task.title, "due_at": task.due_at.isoformat() if task.due_at else None},
                dapr_port=settings.dapr_http_port,
            )

        return task

    def list_tasks(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None,
        sort_by: Optional[str] = "id",
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None,
        overdue: Optional[bool] = None,
        sort_dir: Optional[str] = "asc",
    ) -> List[Task]:
        """List all tasks with optional filtering and sorting.

        Task T033: Implement due-date filtering logic (due_before, due_after, overdue).

        Args:
            search: Case-insensitive search term for titles
            status: Filter by 'complete' or 'incomplete'
            priority: Filter by priority level
            tag: Filter by tag
            sort_by: Sort order ('priority', 'alpha', 'id', 'due_date', 'created_at')
            due_before: Filter tasks due before this datetime
            due_after: Filter tasks due after this datetime
            overdue: Filter only overdue tasks (due_at < now and not completed)
            sort_dir: Sort direction ('asc' or 'desc')

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

        # T033: Apply due-date filters
        if due_before:
            statement = statement.where(Task.due_at < due_before)
        if due_after:
            statement = statement.where(Task.due_at > due_after)

        tasks = list(self.session.exec(statement).all())

        # Apply tag filter (done in Python since JSON querying varies by DB)
        if tag:
            tasks = [t for t in tasks if tag in t.tags]

        # T033: Apply overdue filter (done in Python)
        if overdue is not None:
            now = datetime.utcnow()
            if overdue:
                tasks = [t for t in tasks if t.due_at and not t.completed and t.due_at < now]
            else:
                tasks = [t for t in tasks if not (t.due_at and not t.completed and t.due_at < now)]

        # Apply sorting (T034)
        tasks = self.sort_tasks(tasks, sort_by, sort_dir)

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
        due_at: Optional[datetime] = None,
        remind_at: Optional[datetime] = None,
        recurrence_rule: Optional[RecurrenceRule] = None,
        recurrence_interval: Optional[int] = None,
    ) -> Optional[Task]:
        """Update a task's fields.

        Task T014: Accept and persist due_at and remind_at.
        Task T042: Publish task.updated event after task update.
        Task T060: Schedule/reschedule reminder if remind_at is updated.

        Args:
            task_id: Task identifier
            title: New title (if provided)
            priority: New priority (if provided)
            due_at: New due date (if provided)
            remind_at: New reminder time (if provided)
            recurrence_rule: New recurrence pattern (if provided)
            recurrence_interval: New custom interval (if provided)

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.session.get(Task, task_id)
        if not task:
            return None

        # Track if remind_at changed
        old_remind_at = task.remind_at
        remind_at_changed = remind_at is not None and remind_at != old_remind_at

        if title is not None:
            task.title = title
        if priority is not None:
            task.priority = priority
        if due_at is not None:
            task.due_at = due_at
        if remind_at is not None:
            task.remind_at = remind_at
        if recurrence_rule is not None:
            task.recurrence_rule = recurrence_rule
        if recurrence_interval is not None:
            task.recurrence_interval = recurrence_interval

        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        logger.info(f"Updated task #{task_id}")

        # T042: Publish task.updated event to task-events and task-updates topics
        if self.event_publisher:
            from api.tasks import task_to_dict
            task_snapshot = task_to_dict(task)
            self.event_publisher.publish_sync("task-events", "task.updated", task.id, task_snapshot, actor="user")
            self.event_publisher.publish_sync("task-updates", "task.updated", task.id, task_snapshot, actor="user")

        # T060: Reschedule reminder if remind_at was updated
        if remind_at_changed:
            from services.event_publisher import cancel_reminder_sync, schedule_reminder_sync
            from config import settings

            # Cancel old reminder if it existed
            if old_remind_at:
                cancel_reminder_sync(task_id=task.id, dapr_port=settings.dapr_http_port)

            # Schedule new reminder
            schedule_reminder_sync(
                task_id=task.id,
                remind_at=task.remind_at,
                payload={"title": task.title, "due_at": task.due_at.isoformat() if task.due_at else None},
                dapr_port=settings.dapr_http_port,
            )

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Task T044: Publish task.deleted event after task deletion.
        Task T061: Cancel scheduled reminder when task is deleted.

        Args:
            task_id: Task identifier

        Returns:
            True if deleted, False if not found
        """
        task = self.session.get(Task, task_id)
        if not task:
            return False

        # T044: Capture task snapshot before deletion for event publishing
        if self.event_publisher:
            from api.tasks import task_to_dict
            task_snapshot = task_to_dict(task)

        # T061: Cancel reminder if task had one scheduled
        had_reminder = task.remind_at is not None

        self.session.delete(task)
        self.session.commit()
        logger.info(f"Deleted task #{task_id}")

        # T044: Publish task.deleted event to task-events and task-updates topics
        if self.event_publisher:
            self.event_publisher.publish_sync("task-events", "task.deleted", task_id, task_snapshot, actor="user")
            self.event_publisher.publish_sync("task-updates", "task.deleted", task_id, task_snapshot, actor="user")

        # T061: Cancel reminder job after deletion
        if had_reminder:
            from services.event_publisher import cancel_reminder_sync
            from config import settings
            cancel_reminder_sync(task_id=task_id, dapr_port=settings.dapr_http_port)

        return True

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle the completion status of a task.

        Task T025: Call recurrence spawning logic when task has recurrence_rule
        and is being marked complete.
        Task T043: Publish task.completed event when task is marked complete.
        Task T061: Cancel scheduled reminder when task is completed.

        Args:
            task_id: Task identifier

        Returns:
            Updated Task if found, None otherwise
        """
        task = self.session.get(Task, task_id)
        if not task:
            return None

        was_incomplete = not task.completed
        had_reminder = task.remind_at is not None
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        logger.info(f"Toggled task #{task_id} completion to {task.completed}")

        # T043: Publish task.completed event when marked complete
        if was_incomplete and task.completed:
            if self.event_publisher:
                from api.tasks import task_to_dict
                task_snapshot = task_to_dict(task)
                metadata = {"has_recurrence_rule": task.recurrence_rule is not None}
                self.event_publisher.publish_sync("task-events", "task.completed", task.id, task_snapshot, actor="user", metadata=metadata)
                self.event_publisher.publish_sync("task-updates", "task.completed", task.id, task_snapshot, actor="user")

            # T061: Cancel reminder when task is completed
            if had_reminder:
                from services.event_publisher import cancel_reminder_sync
                from config import settings
                cancel_reminder_sync(task_id=task.id, dapr_port=settings.dapr_http_port)

        # T025: Spawn recurring instance if task has recurrence rule and was just marked complete
        if was_incomplete and task.completed and task.recurrence_rule:
            self.spawn_recurring_instance(task)

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

    def sort_tasks(self, tasks: List[Task], sort_by: Optional[str] = "id", sort_dir: Optional[str] = "asc") -> List[Task]:
        """Sort a list of tasks.

        Task T034: Add due_date and created_at sort options + sort_dir support.

        Args:
            tasks: List of tasks to sort
            sort_by: Sort order ('priority', 'alpha', 'id', 'due_date', 'created_at')
            sort_dir: Sort direction ('asc' or 'desc')

        Returns:
            Sorted list of tasks
        """
        reverse = (sort_dir == "desc")

        if sort_by == "priority":
            priority_order = {Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}
            return sorted(tasks, key=lambda t: priority_order.get(t.priority, 2), reverse=reverse)
        elif sort_by == "alpha":
            return sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)
        elif sort_by == "due_date":
            # Sort by due_date with nulls last
            return sorted(tasks, key=lambda t: (t.due_at is None, t.due_at or datetime.max), reverse=reverse)
        elif sort_by == "created_at":
            return sorted(tasks, key=lambda t: t.created_at or datetime.min, reverse=reverse)
        else:  # Default to 'id'
            return sorted(tasks, key=lambda t: t.id or 0, reverse=reverse)

    def calculate_next_due_date(
        self,
        current_due_at: Optional[datetime],
        rule: RecurrenceRule,
        interval: Optional[int] = None,
    ) -> datetime:
        """Calculate the next due date for a recurring task.

        Task T024: Helper function to compute next due_at based on recurrence rule.

        Args:
            current_due_at: Current due date (or None)
            rule: Recurrence rule
            interval: Custom interval for every_N_days

        Returns:
            Next due date
        """
        base_date = current_due_at or datetime.utcnow()

        if rule == RecurrenceRule.DAILY:
            return base_date + timedelta(days=1)
        elif rule == RecurrenceRule.WEEKLY:
            return base_date + timedelta(weeks=1)
        elif rule == RecurrenceRule.MONTHLY:
            return base_date + relativedelta(months=1)
        elif rule == RecurrenceRule.EVERY_N_DAYS:
            if not interval or interval < 1:
                interval = 1
            return base_date + timedelta(days=interval)
        else:
            # Fallback: daily
            return base_date + timedelta(days=1)

    def spawn_recurring_instance(self, completed_task: Task) -> Task:
        """Create a new task instance for a recurring task.

        Task T026: Implement spawn_recurring_instance() that creates a new task
        with same title/priority/tags/recurrence_rule and next due_at.

        Args:
            completed_task: The completed task with recurrence_rule set

        Returns:
            The newly created recurring task instance
        """
        next_due_at = self.calculate_next_due_date(
            completed_task.due_at,
            completed_task.recurrence_rule,
            completed_task.recurrence_interval,
        )

        # Create new task with same properties but new due date
        new_task = Task(
            title=completed_task.title,
            priority=completed_task.priority,
            tags=completed_task.tags[:],  # Copy tags
            due_at=next_due_at,
            remind_at=None,  # Do not copy remind_at (user must set manually for each instance)
            recurrence_rule=completed_task.recurrence_rule,
            recurrence_interval=completed_task.recurrence_interval,
            completed=False,
        )

        self.session.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)
        logger.info(f"Spawned recurring instance #{new_task.id} from completed task #{completed_task.id}")
        return new_task
