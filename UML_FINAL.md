# PawPal+ System Architecture - Final UML Diagram

## Mermaid Class Diagram

```mermaid
classDiagram
    class Task {
        -String description
        -String time
        -String frequency
        -Boolean completion_status
        -Integer duration_minutes
        -String pet_id
        -String priority
        +mark_complete()
        +mark_incomplete()
        +is_complete() Boolean
        +__str__() String
    }
    
    class Pet {
        -String name
        -String species
        -Integer age
        -Float weight
        -String pet_id
        -List~String~ health_needs
        -Integer daily_activity_minutes
        -List~String~ dietary_restrictions
        -List~String~ allergies
        -List~Task~ tasks
        +update_weight(Float)
        +update_health_needs(List)
        +add_task(Task)
        +remove_task(Task)
        +get_tasks() List~Task~
        +get_incomplete_tasks() List~Task~
        +get_completed_tasks() List~Task~
    }
    
    class Owner {
        -String name
        -String email
        -String phone_number
        -String occupation
        -String owner_id
        -List~Pet~ pets
        +add_pet(Pet)
        +remove_pet(Pet)
        +get_pet_by_name(String) Pet
        +get_pets() List~Pet~
        +get_all_tasks() List~Task~
        +get_all_incomplete_tasks() List~Task~
        +get_tasks_by_pet(String) List~Task~
        +get_pet_count() Integer
    }
    
    class Constraints {
        -String city
        -String climate
        -String weather_condition
        -Boolean has_yard
        -List~Tuple~ available_exercise_hours
        -List~String~ exercise_types
        -Float max_activity_per_hour
        +set_city(String)
        +set_climate(String)
        +set_weather_conditions(List)
        +set_has_yard(Boolean)
        +set_available_exercise_hours(List)
    }
    
    class ScheduleEvent {
        -String task_name
        -String start_time
        -String end_time
        -String location
        -String event_type
        -String priority
        -List~String~ notes
        +get_duration() Integer
        +is_conflicting(ScheduleEvent) Boolean
    }
    
    class Schedule {
        -String date
        -List~ScheduleEvent~ events
        +add_event(ScheduleEvent) Boolean
        +get_events() List~ScheduleEvent~
        +get_date() String
        +get_total_duration() Integer
        +get_wellbeing_score() Float
    }
    
    class Scheduler {
        -Owner owner
        -Constraints constraints
        -Schedule schedule
        +generate_optimal_schedule(String) Schedule
        +sort_tasks_by_time(List) List~Task~
        +filter_tasks_by_status(Boolean) List~Task~
        +filter_tasks_by_pet(String) List~Task~
        +mark_task_complete(String, String) Boolean
        +check_conflicts() List~String~
        +get_all_tasks() List~Task~
        +get_all_incomplete_tasks() List~Task~
        +get_suggestions() List~String~
    }
    
    %% Relationships
    Pet "1" *-- "many" Task : contains
    Owner "1" *-- "many" Pet : owns
    Schedule "1" *-- "many" ScheduleEvent : contains
    Scheduler "1" --> "1" Owner : manages
    Scheduler "1" --> "1" Constraints : applies
    Scheduler "1" --> "1" Schedule : produces
    ScheduleEvent --> "0..1" Task : represents
```

## Architecture Overview

### Core Classes

#### **Task** ➜ Individual Activity
- Represents a single pet care activity (walk, feed, medication, etc.)
- Tracks completion status and frequency (daily/weekly)
- Methods for status tracking

#### **Pet** ➜ Individual Animal
- Represents a specific pet with health/dietary info
- Maintains list of tasks
- Provides task filtering by completion status

#### **Owner** ➜ Orchestrator
- Manages multiple pets
- Aggregates all tasks across pets
- Central data holder for the system

#### **Constraints** ➜ Rules & Limits
- Specifies scheduling boundaries
- Climate, weather, location, availability
- Exercise limits and preferences

#### **Schedule & ScheduleEvent** ➜ Output
- `Schedule`: Daily plan containing events
- `ScheduleEvent`: Individual scheduled activity with time window
- Prevents conflicting events

#### **Scheduler** ➜ Intelligence Engine
- **Phase 3 Logic**: Generates optimal schedule from tasks and constraints
- **Phase 5 Smart Algorithms**:
  - `sort_tasks_by_time()`: Chronological ordering (lambda + time conversion)
  - `filter_tasks_by_status()`: Complete vs incomplete separation
  - `filter_tasks_by_pet()`: Pet-specific task isolation
  - `mark_task_complete()`: Recurring task automation
  - `check_conflicts()`: Detailed conflict warnings
  - `get_suggestions()`: Optimization recommendations

## Data Flow

```
┌─────────────────────────────────────────────────────┐
│                    Streamlit UI (app.py)             │
│  • Owner info form                                   │
│  • Pet management                                    │
│  • Task creation                                     │
│  • Schedule generation button                        │
│  • Smart feature tabs                                │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│             Data Model (pawpal_system.py)            │
│  • Task: description, time, priority, duration      │
│  • Pet: name, species, tasks[]                       │
│  • Owner: name, pets[]                               │
│  • Constraints: location, weather, availability     │
│  • Schedule: events[] for daily plan                 │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│          Scheduler (Intelligence Engine)             │
│  ┌──────────────────────────────────────────┐       │
│  │ Phase 3: Schedule Generation              │       │
│  │ • Optimal scheduling algorithm            │       │
│  │ • Conflict prevention                     │       │
│  │ • Wellbeing scoring                       │       │
│  └──────────────────────────────────────────┘       │
│  ┌──────────────────────────────────────────┐       │
│  │ Phase 5: Smart Algorithms                 │       │
│  │ • sort_tasks_by_time()  ──→ Sorted[]     │       │
│  │ • filter_tasks_by_status() ──→ Complete[]│       │
│  │ • filter_tasks_by_pet() ──→ PetTasks[]   │       │
│  │ • mark_task_complete() ──→ Auto-create   │       │
│  │ • check_conflicts() ──→ Warnings[]        │       │
│  └──────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│           Schedule Output (Display in UI)            │
│  • Time-ordered events                              │
│  • Priority indicators                              │
│  • Conflict warnings                                │
│  • Wellbeing score                                  │
│  • Smart feature filters & sorts                    │
└─────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. **Separation of Concerns**
- **Data**: Task, Pet, Owner classes (simple data holders)
- **Logic**: Scheduler class (all algorithm logic)
- **UI**: app.py (Streamlit components)

### 2. **Smart Algorithm Architecture**
All algorithms in Scheduler class use:
- **Sorting**: Lambda function for time conversion
- **Filtering**: List comprehension for efficient selection
- **Conflict Detection**: Duration overlap checking (not exact time matching)
- **Automation**: Datetime manipulation for recurring tasks

### 3. **Conflict Prevention**
- Schedule.add_event() checks for conflicts before adding
- Scheduler.check_conflicts() reports detailed warnings
- Overlapping events prevented at insertion time

### 4. **Extensibility**
- Easy to add new filters (add method to Scheduler)
- Easy to add new constraints (add field to Constraints)
- Event properties extensible (notes, location, etc.)

## Method Summary by Phase

### **Phase 1-2: Foundation** (Classes & Basic Methods)
- Task: create, mark_complete, is_complete
- Pet: add_task, remove_task, get_tasks
- Owner: add_pet, remove_pet, get_pet_by_name
- Schedule: add_event, get_events, prevent conflicts
- Constraints: set configuration

### **Phase 3: Scheduling Logic** (Algorithm)
- Scheduler: generate_optimal_schedule()
  - Creates schedule with events
  - Orders tasks by priority
  - Prevents time conflicts
  - Calculates wellbeing score

### **Phase 4: UI Integration** (Streamlit)
- app.py: All UI components wired to classes
- Session state persistence
- Form inputs → class instantiation
- Button clicks → method calls

### **Phase 5: Smart Algorithms** (Intelligence)
- Scheduler: sort_tasks_by_time()
- Scheduler: filter_tasks_by_status()
- Scheduler: filter_tasks_by_pet()
- Scheduler: mark_task_complete() (auto-recurring)
- Scheduler: check_conflicts() (warnings)
- Scheduler: get_suggestions() (optimization)

### **Phase 6: Testing** (Validation)
- 30 comprehensive unit tests
- 100% pass rate
- Edge cases covered
- Smart algorithms verified

### **Phase 7: Packaging** (Documentation)
- Enhanced UI with smart features
- Final UML diagram
- Comprehensive README
- AI collaboration reflection

## Final Statistics

- **Lines of Code**: 1,067 (pawpal_system.py)
- **Methods**: 50+ across all classes
- **Smart Algorithms**: 5 core + variations
- **Test Coverage**: 30 tests, 100% pass rate
- **UI Features**: 8 tabs + smart feature toggles
- **Documentation Files**: 10+

## Class Dependencies

```
┌─────────────┐
│   Task      │ (independent)
└──────┬──────┘
       │ "many"
       │
┌──────▼──────┐
│    Pet      │
└──────┬──────┘
       │ "many"
       │
┌──────▼──────────────┐
│     Owner           │
└──────┬──────────────┘
       │
       ├──► ┌─────────────┐
       │    │ Constraints │
       │    └─────────────┘
       │
       └──► ┌──────────────┐
            │ Scheduler    │
            └───────┬──────┘
                    │
                    └──► ┌─────────────────────┐
                         │ Schedule            │
                         │ ├─ ScheduleEvent    │
                         └─────────────────────┘
```

---

**System Design Complete** ✅  
Final revision: March 29, 2026  
All classes implemented and tested
