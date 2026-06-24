# Pet Care App — Class Diagram

```mermaid
classDiagram
    class Owner {
        +String name
        +List~Pet~ pets
        +List~Task~ tasks
        +addPet(pet) void
        +addTask(task) void
        +removeTask(task) void
    }

    class Pet {
        +String name
        +Owner owner
        +List~Task~ tasks
    }

    class Task {
        +String description
        +Owner owner
        +Pet pet
        +int priority
        +addPriority(priority) void
        +isCompleted() bool
    }

    class Scheduler {
        +int priority
        +DateTime time
        +isNow() bool
    }

    Owner "1" --> "0..*" Pet : owns
    Owner "1" --> "0..*" Task : manages
    Pet "1" --> "0..*" Task : has
    Task "1" --> "1" Scheduler : scheduled by
```
