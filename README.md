# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
This is what the app's CLI output looks like:

```
# Today's Schedule
# - 08:00: Feed Chewy (Chewy)
# - 17:00: Walk Chewy (Chewy)
# - 09:00: Feed Bella (Bella)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

What the test covers:
The test covers sorting correctness logic, verifying that tasks are returned in chronological order. It also confirms that marking a daily task complete creates a new(recurring) task for the following day. Lastly, it verifies that the scheduler detects time conflict for tasks. 

Sample test output:
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.4.1, pluggy-1.6.0 -- C:\Users\jaket\AppData\Local\Programs\Python\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\jaket\CodePath\Week-4\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collecting ... collected 14 items

tests/test_pawpal.py::test_task_completion PASSED                        [7%]
tests/test_pawpal.py::test_task_addition_to_pet PASSED                   [14%]
tests/test_pawpal.py::test_sort_by_time_orders_earliest_first PASSED     [21%]
tests/test_pawpal.py::test_sort_by_time_puts_unscheduled_tasks_last PASSED [28%]
tests/test_pawpal.py::test_due_now_orders_by_priority_desc_then_time_asc PASSED [35%]
tests/test_pawpal.py::test_due_now_excludes_future_completed_and_unscheduled_tasks PASSED [42%]
tests/test_pawpal.py::test_complete_recurring_task_anchors_next_occurrence_to_original_schedule PASSED [50%]
tests/test_pawpal.py::test_complete_recurring_task_late_does_not_drift_from_completion_time PASSED [57%]
tests/test_pawpal.py::test_complete_non_recurring_task_returns_none PASSED [64%]
tests/test_pawpal.py::test_complete_recurring_task_without_scheduled_time_returns_none PASSED [71%]
tests/test_pawpal.py::test_scheduler_complete_task_registers_next_occurrence_with_pet_and_owner PASSED [78%]
tests/test_pawpal.py::test_find_conflicts_groups_same_time_tasks_across_pets PASSED [85%]
tests/test_pawpal.py::test_find_conflicts_ignores_completed_and_unscheduled_tasks PASSED [92%]
tests/test_pawpal.py::test_conflict_warnings_format_and_no_pet_label PASSED [100%]

============================= 14 passed in 0.16s ==============================

Confidence level: **** (4 Stars)

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time() | ordered by schelduled time |
| Filtering | filter_tasks() | filters by pets |
| Conflict handling | Scheduler.find_conflicts(), Scheduler.conflict_warnings() | detects overlapping time slots, returns conflict messages |
| Recurring tasks | Task.complete(), Scheduler.complete_task() | daily recurring tasks |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
