# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
UML Design:
|-----------------------|
|   Owner               |
|-----------------------|
|+name: str             |
|+pets: list[Pet]       |
|-----------------------|
|+addPet(pet): void     |
|+addTask(task): void   |
|+removeTask(task): void|
|-----------------------|
         | 1
         | owns
         | *
         V
|-----------------------|
|    Pet                |
|-----------------------|
|+name: str             |
|+owner: Owner          |
|+tasks: list[Task]     |
|-----------------------|
Classes I chose:
- Owner: contains data of the pet owner, the pet, and a list of task(s). This class is responsible to hold attributes, methods and basic information pertaining to the owner.
- Pet: a pure data class that contains the name, owner and task(s) of a pet. This class provides data of the pet.
- Task: manages the task(s) of the owner and pet, filter tasks by priority, and tracks the status of tasks.
- Scheduler: contains attributes by which tasks are scheduled.

Three actions:
- Adding a pet
- Schedule feeding
- Schedule a walk

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Changes:
- Added scheduler attribute to Task class because a task needs to be scheduled and linked to Scheduler class.
- Removed priority attribute from Scheduler so that only it is set based on the task. It now only lives in the Task class.
- Added completed attribute to Task class to track the completion of a task.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
