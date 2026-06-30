from pawpal_system import Pet, Task


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
