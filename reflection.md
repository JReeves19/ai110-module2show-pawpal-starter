# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The UML design contains four classes: Owner, Pet, Task and Scheduler. These classes contain attributes and methods that are connects with each other to make the system work. How these class are related and work together:
- An `Owner` can own multiple `Pets`.
- An `Owner` can manage multiple `Tasks`.
- A `Pet` can have multiple `Tasks`.
- A `Scheduler` can schedule multiple `Tasks`.

Classes I chose:
- Owner: contains data of the pet owner, the pet, and a list of task(s). This class is responsible to hold attributes, methods and basic information pertaining to the owner.
- Pet: a pure data class that contains the name, owner and task(s) of a pet. This class provides data of the pet.
- Task: manages the task(s) of the owner and pet, filter tasks by priority, and tracks the status of tasks.
- Scheduler: contains attributes by which tasks are scheduled.

Three actions:
- Adding a pet
- Assign a task to a pet
- Choose a priority

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

My scheduler only looks at two things: scheduled time and priority. Time decides whether a task is due yet and whether two tasks land on the same slot. Priority decides which task comes first when more than one is due. I picked these two because they were the minimum needed to answer "what should I do next". Things like task duration or owner preferences would be nice later, but the app doesn't need them to work.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler doesn't keep any separate lookup table to speed up queries like "what's due now" or "what conflicts with what." Every time I ask it one of these questions, it just scans through all the tasks again instead of remembering the answer from last time. The tradeoff is that this makes each query a little slower as the number of tasks grows, but it also means there's no extra bookkeeping to keep in sync. I never have to worry about a cached list getting out of date when a task is added, completed, or removed. For a pet-care app where one owner might have a few dozen tasks at most, that simplicity is worth more than the small speed gain, so I think it's a reasonable tradeoff.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

During this project, I used AI tools to brainstorm better design ideas and approaches. It helped me to design and build simple algorithms that made my backend smart. The most helpful prompts in this process were brainstorming and planning prompts. The AI tool read through my codebase to get more context, and then brainstormed some design ideas to my the app better. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I asked for time conflict detection, the AI first built it to return the actual list of conflicting Task objects grouped together. That wasn't what I wanted, so I told it I needed something lighter: a simple warning message instead of raw task data. It rewrote the feature as a method that returns readable strings like "Conflict at 9:00: Feed Chewy, Walk Chewy" instead. I verified it worked by running the tasks through it myself and checking the warning only showed up when tasks actually shared the same time.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I wrote tests for the three core behaviors of the scheduler: sorting tasks by time, recurrence (completing a task creates the next occurrence), and conflict detection (flagging tasks scheduled at the same time). I also tested edge cases like tasks with no scheduled time, already-completed tasks, and tasks with no pet assigned. These mattered because sorting, recurrence, and conflicts are the parts of the app most likely to silently return the wrong order or miss a case if the logic is even slightly off.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident the core logic works, since all 14 tests pass and cover the main paths plus several edge cases. I'm less confident about things I haven't tested yet, like double-completing the same task (which could create duplicate recurring tasks) or mixing timezone-aware and naive datetimes. If I had more time, I'd test those, plus what happens when a task is reassigned from one pet to another.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with how the scheduling methods ended up reusing each other instead of each one reinventing its own logic. `due_now()` is really just `pending()` plus a time filter plus a sort; `find_conflicts()` reuses the same "pending tasks with a scheduled time" filter. Because of that, I could test each small piece on its own and trust the bigger methods that were built out of them, and I got the whole thing working end to end; backend logic, 14 passing tests, and a real Streamlit UI that shows the sorted schedule and conflict warnings live.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Two things stand out. First, `Task.complete()` and `Scheduler.complete_task()` (the recurrence logic) are fully built and tested, but I never wired a "mark complete" button into the actual Streamlit UI, so a user can't see recurrence happen live, only in tests. Second, the original scenario mentioned task duration as something to track, but my `Task` class never grew a duration field. Priority and time turned out to be enough for the scheduler to work, but duration would matter if I ever wanted the plan to account for how long a task actually takes.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The biggest thing I learned is that it's worth pinning down small design decisions in plain language before any code gets written. Things like "does a tie in priority break by time?" or "should this return raw data or a message?" Every time I skipped straight to "just build it," I ended up with something technically working but not what I actually wanted, and had to redo it. Answering those questions first, even in one sentence, saved way more time than it cost.
