"""PawPal — pet care app domain model.

Skeleton generated from the UML class diagram (see pet-care-class-diagram.md).
Dataclasses are used for the data-holding objects (Pet, Task, Scheduler);
Owner is a plain class since it orchestrates the relationships.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Pet:
    name: str
    owner: "Owner | None" = None
    tasks: list["Task"] = field(default_factory=list)


@dataclass
class Task:
    description: str
    owner: "Owner | None" = None
    pet: Pet | None = None
    priority: int = 0

    def add_priority(self, priority: int) -> None:
        """Set/update this task's priority."""
        raise NotImplementedError

    def is_completed(self) -> bool:
        """Return True if the task has been completed."""
        raise NotImplementedError


@dataclass
class Scheduler:
    priority: int = 0
    time: datetime | None = None

    def is_now(self) -> bool:
        """Return True if this scheduled task is due right now."""
        raise NotImplementedError


class Owner:
    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: list[Pet] = []
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        raise NotImplementedError

    def add_task(self, task: Task) -> None:
        """Add a task for this owner."""
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        """Remove a task from this owner."""
        raise NotImplementedError
