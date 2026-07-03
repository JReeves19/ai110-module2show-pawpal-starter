from datetime import datetime

from pawpal_system import Pet, Owner, Task, Scheduler

if __name__ == '__main__':
    owner = Owner("John")
    scheduler = Scheduler()

    dog = Pet("Chewy")
    cat = Pet("Bella")
    owner.add_pet(dog)
    owner.add_pet(cat)

    feed_dog = Task("Feed Chewy", priority=2, scheduled_time=datetime(2026, 6, 29, 8, 0))
    feed_cat = Task("Feed Bella", priority=2, scheduled_time=datetime(2026, 6, 29, 9, 0))
    brush_dog = Task("Brush Chewy", priority=1, scheduled_time=datetime(2026, 6, 29, 9, 0))
    medicine_dog = Task("Give Chewy medicine", priority=4, scheduled_time=datetime(2026, 6, 29, 9, 0))
    vet_dog = Task("Vet checkup", priority=5, scheduled_time=datetime(2026, 6, 29, 10, 30))
    walk_dog = Task("Walk Chewy", priority=1, scheduled_time=datetime(2026, 6, 29, 17, 0))
    groom_cat = Task("Groom Bella", priority=3, scheduled_time=datetime(2026, 6, 29, 7, 0), completed=True)

    # Registered out of chronological order on purpose, to prove the
    # scheduling/sorting methods don't depend on insertion order.
    # feed_cat, brush_dog, and medicine_dog are all scheduled for 09:00 --
    # two conflict with each other on the same pet (Chewy), and both
    # conflict with feed_cat on a different pet (Bella) -- to exercise
    # conflict_warnings().
    for task, pet in [
        (walk_dog, dog),
        (vet_dog, dog),
        (groom_cat, cat),
        (feed_cat, cat),
        (medicine_dog, dog),
        (feed_dog, dog),
        (brush_dog, dog),
    ]:
        pet.add_task(task)
        owner.add_task(task)
        scheduler.schedule(task)

    print("Full Schedule (earliest to latest)")
    for task in scheduler.sort_by_time():
        status = " (completed)" if task.is_completed() else ""
        print(f"- {task.scheduled_time.strftime('%H:%M')}: {task.description} ({task.pet.name}){status}")

    now = datetime(2026, 6, 29, 11, 0)
    print(f"\nDue Now (as of {now.strftime('%H:%M')}, highest priority first)")
    for task in scheduler.due_now(now):
        print(f"- {task.scheduled_time.strftime('%H:%M')} [priority {task.priority}]: {task.description} ({task.pet.name})")

    print("\nJohn's Pending Tasks (earliest to latest)")
    for task in scheduler.sort_by_time(owner.pending()):
        print(f"- {task.scheduled_time.strftime('%H:%M')}: {task.description} ({task.pet.name})")

    print("\nCompleted Tasks")
    for task in owner.completed():
        print(f"- {task.description} ({task.pet.name})")

    print("\nSchedule Conflicts")
    warnings = scheduler.conflict_warnings()
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- none")
