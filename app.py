from datetime import date, datetime, time

import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler

PRIORITY_LEVELS = {"low": 1, "medium": 2, "high": 3}

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner = st.session_state.owner

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
scheduler = st.session_state.scheduler

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name))
    st.success(f"Added {pet_name} to {owner.name}'s pets.")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": pet.name} for pet in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed straight into the Scheduler below.")

if not owner.pets:
    st.info("Add a pet above before adding tasks.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        pet_choice = st.selectbox("Pet", [pet.name for pet in owner.pets])
    with col3:
        priority_choice = st.selectbox("Priority", list(PRIORITY_LEVELS), index=2)
    with col4:
        scheduled_time_input = st.time_input("Scheduled time", value=time(8, 0))

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == pet_choice)
        task = Task(
            task_title,
            priority=PRIORITY_LEVELS[priority_choice],
            scheduled_time=datetime.combine(date.today(), scheduled_time_input),
        )
        pet.add_task(task)
        owner.add_task(task)
        scheduler.schedule(task)
        st.success(f"Added '{task_title}' for {pet.name} at {scheduled_time_input.strftime('%H:%M')}.")

if scheduler.tasks:
    st.write("Current tasks (earliest to latest):")
    st.table(
        [
            {
                "time": task.scheduled_time.strftime("%H:%M"),
                "title": task.description,
                "pet": task.pet.name if task.pet else "—",
                "priority": task.priority,
                "completed": task.is_completed(),
            }
            for task in scheduler.sort_by_time()
        ]
    )

    for warning in scheduler.conflict_warnings():
        st.warning(warning)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Orders today's pending tasks and flags any that land at the same time.")

if st.button("Generate schedule"):
    plan = scheduler.sort_by_time(owner.pending())
    if not plan:
        st.info("No pending tasks to schedule yet.")
    else:
        st.markdown("**Today's plan (earliest to latest):**")
        st.table(
            [
                {
                    "time": task.scheduled_time.strftime("%H:%M"),
                    "title": task.description,
                    "pet": task.pet.name if task.pet else "—",
                    "priority": task.priority,
                }
                for task in plan
            ]
        )

    conflicts = scheduler.conflict_warnings(owner.pending())
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No conflicts — the schedule is clear.")
