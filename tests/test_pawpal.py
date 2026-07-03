from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    task = Task("Walk the dog")
    assert task.is_completed() is False

    task.completed = True

    assert task.is_completed() is True


def test_task_addition_to_pet():
    pet = Pet("Chewy")
    task = Task("Feed Chewy")

    before_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == before_count + 1


# --- Sorting correctness ---------------------------------------------------

def test_sort_by_time_orders_earliest_first():
    scheduler = Scheduler()
    late = Task("late", scheduled_time=datetime(2026, 1, 1, 10, 0))
    early = Task("early", scheduled_time=datetime(2026, 1, 1, 8, 0))
    middle = Task("middle", scheduled_time=datetime(2026, 1, 1, 9, 0))
    for task in (late, early, middle):
        scheduler.schedule(task)

    assert scheduler.sort_by_time() == [early, middle, late]


def test_sort_by_time_puts_unscheduled_tasks_last():
    scheduler = Scheduler()
    scheduled = Task("scheduled", scheduled_time=datetime(2026, 1, 1, 10, 0))
    unscheduled = Task("unscheduled")
    scheduler.schedule(unscheduled)
    scheduler.schedule(scheduled)

    assert scheduler.sort_by_time() == [scheduled, unscheduled]


def test_due_now_orders_by_priority_desc_then_time_asc():
    scheduler = Scheduler()
    now = datetime(2026, 1, 1, 12, 0)
    high_earlier = Task("high-earlier", priority=5, scheduled_time=now - timedelta(hours=2))
    high_later = Task("high-later", priority=5, scheduled_time=now - timedelta(hours=1))
    low = Task("low", priority=1, scheduled_time=now - timedelta(hours=3))
    for task in (high_later, low, high_earlier):
        scheduler.schedule(task)

    assert scheduler.due_now(now) == [high_earlier, high_later, low]


def test_due_now_excludes_future_completed_and_unscheduled_tasks():
    scheduler = Scheduler()
    now = datetime(2026, 1, 1, 12, 0)
    due = Task("due", scheduled_time=now)
    future = Task("future", scheduled_time=now + timedelta(hours=1))
    completed = Task("completed", scheduled_time=now - timedelta(hours=1), completed=True)
    unscheduled = Task("unscheduled")
    for task in (due, future, completed, unscheduled):
        scheduler.schedule(task)

    assert scheduler.due_now(now) == [due]


# --- Recurrence logic --------------------------------------------------------

def test_complete_recurring_task_anchors_next_occurrence_to_original_schedule():
    scheduled = datetime(2026, 1, 1, 9, 0)
    task = Task("Feed", scheduled_time=scheduled, recurrence=timedelta(days=1))

    next_task = task.complete()

    assert task.is_completed() is True
    assert next_task is not None
    assert next_task.scheduled_time == scheduled + timedelta(days=1)
    assert next_task.recurrence == timedelta(days=1)
    assert next_task.is_completed() is False


def test_complete_recurring_task_late_does_not_drift_from_completion_time():
    scheduled = datetime(2026, 1, 1, 9, 0)
    task = Task("Feed", scheduled_time=scheduled, recurrence=timedelta(days=1))

    # Completing it "late" (well after its scheduled time) must not push the
    # next occurrence later than scheduled + recurrence.
    next_task = task.complete()

    assert next_task.scheduled_time == scheduled + timedelta(days=1)


def test_complete_non_recurring_task_returns_none():
    task = Task("One-off", scheduled_time=datetime(2026, 1, 1, 9, 0))

    assert task.complete() is None
    assert task.is_completed() is True


def test_complete_recurring_task_without_scheduled_time_returns_none():
    task = Task("No time", recurrence=timedelta(days=1))

    assert task.complete() is None
    assert task.is_completed() is True


def test_scheduler_complete_task_registers_next_occurrence_with_pet_and_owner():
    scheduler = Scheduler()
    owner = Owner("Jake")
    pet = Pet("Chewy")
    owner.add_pet(pet)

    task = Task("Walk", scheduled_time=datetime(2026, 1, 1, 9, 0), recurrence=timedelta(days=1))
    pet.add_task(task)
    owner.add_task(task)
    scheduler.schedule(task)

    next_task = scheduler.complete_task(task)

    assert next_task is not None
    assert next_task.task_id in scheduler.tasks
    assert next_task.task_id in pet.tasks
    assert next_task.task_id in owner.tasks
    assert next_task.pet is pet
    assert next_task.owner is owner


# --- Conflict detection ------------------------------------------------------

def test_find_conflicts_groups_same_time_tasks_across_pets():
    scheduler = Scheduler()
    when = datetime(2026, 1, 1, 9, 0)
    pet_a = Pet("Chewy")
    pet_b = Pet("Milo")
    walk_chewy = Task("Walk Chewy", pet=pet_a, scheduled_time=when)
    walk_milo = Task("Walk Milo", pet=pet_b, scheduled_time=when)
    unrelated = Task("Unrelated", scheduled_time=when + timedelta(hours=1))
    for task in (walk_chewy, walk_milo, unrelated):
        scheduler.schedule(task)

    conflicts = scheduler.find_conflicts()

    assert conflicts == [[walk_chewy, walk_milo]]


def test_find_conflicts_ignores_completed_and_unscheduled_tasks():
    scheduler = Scheduler()
    when = datetime(2026, 1, 1, 9, 0)
    pending = Task("pending", scheduled_time=when)
    completed = Task("completed", scheduled_time=when, completed=True)
    unscheduled = Task("unscheduled")
    for task in (pending, completed, unscheduled):
        scheduler.schedule(task)

    assert scheduler.find_conflicts() == []


def test_conflict_warnings_format_and_no_pet_label():
    scheduler = Scheduler()
    when = datetime(2026, 1, 1, 9, 0)
    pet = Pet("Chewy")
    walk = Task("Walk", pet=pet, scheduled_time=when)
    feed = Task("Feed", scheduled_time=when)  # no pet assigned
    scheduler.schedule(walk)
    scheduler.schedule(feed)

    warnings = scheduler.conflict_warnings()

    assert len(warnings) == 1
    assert "2026-01-01 09:00" in warnings[0]
    assert "Walk (Chewy)" in warnings[0]
    assert "Feed (no pet)" in warnings[0]
