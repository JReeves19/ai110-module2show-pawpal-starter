from datetime import datetime

from pawpal_system import Pet, Owner, Task, Scheduler

if __name__ == '__main__':
    owner = Owner("John")

    dog = Pet("Chewy")
    cat = Pet("Bella")
    owner.add_pet(dog)
    owner.add_pet(cat)

    feed_dog = Task("Feed Chewy", pet=dog, scheduled_time=datetime(2026, 6, 29, 8, 0))
    walk_dog = Task("Walk Chewy", pet=dog, scheduled_time=datetime(2026, 6, 29, 17, 0))
    feed_cat = Task("Feed Bella", pet=cat, scheduled_time=datetime(2026, 6, 29, 9, 0))

    owner.add_task(feed_dog)
    owner.add_task(walk_dog)
    owner.add_task(feed_cat)

    print("Today's Schedule")
    for task in owner.tasks.values():
        print(f"- {task.scheduled_time.strftime('%H:%M')}: {task.description} ({task.pet.name})")
