"""PawPal — pet care app domain model.

Skeleton generated from the UML class diagram (see pet-care-class-diagram.md).
Dataclasses are used for the data-holding objects (Pet, Task, Scheduler);
Owner is a plain class since it orchestrates the relationships.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Pet:
    name: str
    owner: "Owner | None" = None
    tasks: dict[str, "Task"] = field(default_factory=dict)

    def add_task(self, task: "Task") -> None:
        """Attach a task to this pet and point the task back at this pet."""
        self.tasks[task.task_id] = task
        task.pet = self


@dataclass
class Task:
    description: str
    task_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    owner: "Owner | None" = None
    pet: Pet | None = None
    priority: int = 0
    scheduled_time: datetime | None = None
    completed: bool = False 

    def add_priority(self, priority: int) -> None:
        """Update this task's priority level."""
        raise NotImplementedError

    def is_completed(self) -> bool:
        """Check whether this task has been marked as completed."""
        return self.completed


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

    def due_now(self, now: datetime) -> list[Task]:
        """Return incomplete tasks due at or before `now`, highest priority first."""
        raise NotImplementedError


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
