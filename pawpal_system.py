"""PawPal — pet care app domain model.

Skeleton generated from the UML class diagram (see pet-care-class-diagram.md).
Dataclasses are used for the data-holding objects (Pet, Task, Scheduler);
Owner is a plain class since it orchestrates the relationships.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import datetime, timedelta


def filter_tasks(tasks: Iterable["Task"], predicate: Callable[["Task"], bool]) -> list["Task"]:
    """Return the tasks in `tasks` for which `predicate` returns True."""
    return [task for task in tasks if predicate(task)]


@dataclass
class Pet:
    name: str
    owner: "Owner | None" = None
    tasks: dict[str, "Task"] = field(default_factory=dict)

    def add_task(self, task: "Task") -> None:
        """Attach a task to this pet and point the task back at this pet."""
        self.tasks[task.task_id] = task
        task.pet = self

    def pending(self) -> list["Task"]:
        """Return this pet's tasks that are not yet completed."""
        return filter_tasks(self.tasks.values(), lambda t: not t.is_completed())

    def completed(self) -> list["Task"]:
        """Return this pet's tasks that are already completed."""
        return filter_tasks(self.tasks.values(), lambda t: t.is_completed())


@dataclass
class Task:
    description: str
    task_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    owner: "Owner | None" = None
    pet: Pet | None = None
    priority: int = 0
    scheduled_time: datetime | None = None
    completed: bool = False
    recurrence: timedelta | None = None

    def add_priority(self, priority: int) -> None:
        """Update this task's priority level."""
        self.priority = priority

    def is_completed(self) -> bool:
        """Check whether this task has been marked as completed."""
        return self.completed

    def complete(self) -> "Task | None":
        """Mark this task completed and, if it recurs, return the next occurrence.

        The next occurrence is anchored to this task's original `scheduled_time`
        (not to whenever it was actually completed), so a recurring task doesn't
        drift later each time it's finished late.
        """
        self.completed = True
        if self.recurrence is None or self.scheduled_time is None:
            return None
        return Task(
            description=self.description,
            owner=self.owner,
            pet=self.pet,
            priority=self.priority,
            scheduled_time=self.scheduled_time + self.recurrence,
            recurrence=self.recurrence,
        )


@dataclass
class Scheduler:
    """Central scheduler shared across the app"""

    tasks: dict[str, Task] = field(default_factory=dict)

    def schedule(self, task: Task) -> None:
        """Add a task to the scheduler, replacing any existing task with the same id."""
        self.tasks[task.task_id] = task

    def unschedule(self, task: Task) -> None:
        """Remove a task from the scheduler if it's present."""
        self.tasks.pop(task.task_id, None)

    def complete_task(self, task: Task) -> Task | None:
        """Mark `task` completed and, if it recurs, schedule and return the next occurrence.

        The new occurrence is registered with the same pet and owner as `task`
        (via their own `add_task`), in addition to this scheduler.
        """
        next_task = task.complete()
        if next_task is None:
            return None
        if next_task.pet is not None:
            next_task.pet.add_task(next_task)
        if next_task.owner is not None:
            next_task.owner.add_task(next_task)
        self.schedule(next_task)
        return next_task

    def pending(self) -> list[Task]:
        """Return scheduled tasks that are not yet completed."""
        return filter_tasks(self.tasks.values(), lambda t: not t.is_completed())

    def completed(self) -> list[Task]:
        """Return scheduled tasks that are already completed."""
        return filter_tasks(self.tasks.values(), lambda t: t.is_completed())

    def sort_by_time(self, tasks: Iterable[Task] | None = None) -> list[Task]:
        """Return `tasks` (or all scheduled tasks) ordered by scheduled_time, earliest first.

        Tasks with no scheduled_time sort last.
        """
        source = self.tasks.values() if tasks is None else tasks
        return sorted(source, key=lambda t: (t.scheduled_time is None, t.scheduled_time))

    def due_now(self, now: datetime) -> list[Task]:
        """Return incomplete tasks due at or before `now`, highest priority first,
        breaking priority ties by earliest scheduled_time."""
        due = filter_tasks(
            self.pending(),
            lambda t: t.scheduled_time is not None and t.scheduled_time <= now,
        )
        return sorted(due, key=lambda t: (-t.priority, t.scheduled_time))

    def find_conflicts(self, tasks: Iterable[Task] | None = None) -> list[list[Task]]:
        """Group pending tasks that share the exact same scheduled_time.

        Grouping ignores which pet a task belongs to, since one owner can't
        do two things at once regardless of pet. Pass a pre-filtered iterable
        (e.g. `owner.pending()`) to scope the check to a single owner instead
        of every task in the scheduler.
        """
        source = self.tasks.values() if tasks is None else tasks
        candidates = filter_tasks(
            source, lambda t: not t.is_completed() and t.scheduled_time is not None
        )

        by_time: dict[datetime, list[Task]] = {}
        for task in candidates:
            by_time.setdefault(task.scheduled_time, []).append(task)

        groups = [group for group in by_time.values() if len(group) > 1]
        groups.sort(key=lambda group: group[0].scheduled_time)
        return groups

    def conflict_warnings(self, tasks: Iterable[Task] | None = None) -> list[str]:
        """Return one human-readable warning per group of same-time conflicts."""
        warnings = []
        for group in self.find_conflicts(tasks):
            when = group[0].scheduled_time.strftime("%Y-%m-%d %H:%M")
            names = ", ".join(
                f"{t.description} ({t.pet.name if t.pet else 'no pet'})" for t in group
            )
            warnings.append(f"Conflict at {when}: {names}")
        return warnings


class Owner:
    def __init__(self, name: str) -> None:
        """Create an owner with no pets or tasks yet."""
        self.name = name
        self.pets: list[Pet] = []
        self.tasks: dict[str, Task] = {}

    def add_pet(self, pet: Pet) -> None:
        """Attach a pet to this owner and point the pet back at this owner."""
        if pet not in self.pets: 
            self.pets.append(pet)
        pet.owner = self 

    def add_task(self, task: Task) -> None:
        """Attach a task to this owner and point the task back at this owner."""
        self.tasks[task.task_id] = task  
        task.owner = self 

    def remove_task(self, task: Task) -> None:
        """Remove a task from this owner and clear its owner link if it pointed here."""
        self.tasks.pop(task.task_id, None)
        if task.owner is self:
            task.owner = None

    def pending(self) -> list[Task]:
        """Return this owner's tasks that are not yet completed."""
        return filter_tasks(self.tasks.values(), lambda t: not t.is_completed())

    def completed(self) -> list[Task]:
        """Return this owner's tasks that are already completed."""
        return filter_tasks(self.tasks.values(), lambda t: t.is_completed())
