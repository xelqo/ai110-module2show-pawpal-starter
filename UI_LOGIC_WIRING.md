# UI to Logic Wiring: Complete Data Flow Analysis

## Overview

Your `app.py` is now **fully wired** to the `pawpal_system.py` backend. This document shows exactly how user actions in the Streamlit UI trigger class methods and update the persistent session state vault.

---

## 1. Adding a Pet: Complete Data Flow

### User Action in UI
```
Owner enters: "Mochi" (name) + "dog" (species)
              ↓
         Clicks "➕ Add Pet" button
```

### Code in app.py (Lines 78-92)
```python
if st.button("➕ Add Pet", key="add_pet_btn"):
    if new_pet_name:
        # STEP 1: Create Pet object using Pet.__init__()
        new_pet = Pet(
            name=new_pet_name,           # "Mochi"
            species=new_pet_species,      # "dog"
            age=1,
            weight=50.0,
            pet_id=f"pet_{len(st.session_state['pets']) + 1}",
            daily_activity_minutes=60
        )
        
        # STEP 2: Add to session state vault
        st.session_state['pets'].append(new_pet)
        
        # STEP 3: Call Owner.add_pet() method
        owner.add_pet(new_pet)
        
        # STEP 4: Show success and refresh UI
        st.success(f"✅ {new_pet_name} the {new_pet_species} added!")
        st.rerun()
```

### Class Methods Called

#### 1. **Pet.__init__()** (pawpal_system.py)
```python
class Pet:
    def __init__(self, name, species, age, weight, pet_id, daily_activity_minutes):
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.pet_id = pet_id
        self.daily_activity_minutes = daily_activity_minutes
        self.tasks = []  # Empty task list
        # ... other attributes
```

**What it does:** Creates a new Pet object with empty task list and default properties.

#### 2. **Owner.add_pet(pet)** (pawpal_system.py, ~line 400)
```python
def add_pet(self, pet):
    """Adds a pet to the owner's pet list."""
    if pet not in self.pets:
        self.pets.append(pet)
        return True
    return False
```

**What it does:** Adds the Pet object to owner's `self.pets` list so the Owner can manage this pet.

### Session State Update

```
st.session_state['pets'].append(new_pet)
    ↓
st.session_state['owner'].pets.append(new_pet)  # Via owner.add_pet()
    ↓
Vault now contains:
{
  'owner': Owner(pets=[Mochi(dog), ...]),
  'pets': [Mochi(dog), ...]
}
```

### UI Update Flow

```
1. Button clicked
   ↓
2. Pet object created
   ↓
3. Pet added to vault (st.session_state['pets'])
   ↓
4. Owner.add_pet() called (updates owner.pets list)
   ↓
5. st.success() displays confirmation
   ↓
6. st.rerun() reruns script top-to-bottom
   ↓
7. Display current pets section (Lines 97-108) runs with NEW pet data
   ↓
8. UI shows: "Your Pets (stored in vault): 🐾 Mochi (dog)" ✅
```

### Why st.rerun()?

Streamlit is **stateless** - it reruns your code top-to-bottom on every interaction. When you:
- Add a pet
- Click delete
- Change owner name
- Add a task

You need to call `st.rerun()` to force the script to rerun and display updated data from the vault.

---

## 2. Adding a Task: Complete Data Flow

### User Action in UI
```
Owner enters: "Morning walk" (title) + 20 (minutes) + "high" (priority)
              ↓
         Clicks "➕ Add Task" button
```

### Code in app.py (Lines 130-145)
```python
if st.button("➕ Add Task", key="add_task_btn"):
    if task_title:
        # STEP 1: Create Task object using Task.__init__()
        task = Task(
            description=task_title,      # "Morning walk"
            time="09:00",
            frequency="daily",
            duration_minutes=int(duration),  # 20
            priority=priority            # "high"
        )
        
        # STEP 2: Add to session state vault
        st.session_state['tasks'].append(task)
        
        # STEP 3: Show success and refresh UI
        st.success(f"✅ Task '{task_title}' added to vault!")
        st.rerun()
```

### Class Method Called

#### Task.__init__() (pawpal_system.py)
```python
class Task:
    def __init__(self, description, time, frequency, duration_minutes, priority):
        self.description = description
        self.time = time
        self.frequency = frequency
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.completion_status = False  # Defaults to incomplete
        # ... other attributes
```

**What it does:** Creates a Task object that's not yet assigned to any pet.

### Session State Update

```
st.session_state['tasks'].append(task)
    ↓
Vault now contains:
{
  'tasks': [
    Task("Morning walk", duration=20, priority="high"),
    Task("Feeding", duration=10, priority="high"),
    ...
  ]
}
```

### Display Current Tasks (Lines 147-162)

After `st.rerun()`, this section displays all tasks:

```python
if st.session_state['tasks']:
    st.write("**Tasks in Vault (will be assigned to pets):**")
    task_df = {
        "Task": [t.description for t in st.session_state['tasks']],
        "Duration (min)": [t.duration_minutes for t in st.session_state['tasks']],
        "Priority": [t.priority for t in st.session_state['tasks']],
        "Status": [("✓" if t.is_complete() else "○") for t in st.session_state['tasks']]
    }
    st.table(task_df)
```

### UI Update Flow

```
1. Button clicked
   ↓
2. Task object created
   ↓
3. Task added to vault (st.session_state['tasks'])
   ↓
4. st.success() displays confirmation
   ↓
5. st.rerun() reruns script
   ↓
6. Task table section (Lines 147-162) runs with NEW task data
   ↓
7. UI shows: "Morning walk | 20 min | high | ○" ✅
```

---

## 3. Deleting a Pet: Complete Data Flow

### User Action in UI
```
Owner clicks "🗑️" delete button next to "Mochi (dog)"
              ↓
         Button triggers with key="delete_pet_0"
```

### Code in app.py (Lines 103-108)
```python
if st.button("🗑️", key=f"delete_pet_{i}"):
    # STEP 1: Remove from vault list
    st.session_state['pets'].pop(i)
    
    # STEP 2: Call Owner.remove_pet() method
    owner.remove_pet(pet)
    
    # STEP 3: Show success and refresh UI
    st.success("Pet removed!")
    st.rerun()
```

### Class Method Called

#### Owner.remove_pet(pet) (pawpal_system.py)
```python
def remove_pet(self, pet):
    """Removes a pet from the owner's pet list."""
    if pet in self.pets:
        self.pets.remove(pet)
        return True
    return False
```

**What it does:** Removes the Pet from owner's `self.pets` list, so owner no longer manages this pet.

### Session State Update

```
st.session_state['pets'].pop(0)  # Remove Mochi
owner.remove_pet(mochi_pet)      # Update owner's list
    ↓
Vault now contains:
{
  'owner': Owner(pets=[]),  # Mochi removed
  'pets': []                # Mochi removed
}
```

---

## 4. Generating a Schedule: Complete Data Flow

### User Action in UI
```
Owner has:
  - At least 1 pet (e.g., "Mochi")
  - At least 1 task (e.g., "Morning walk")
              ↓
         Clicks "🔄 Generate Schedule" button
```

### Code in app.py (Lines 175-205)
```python
if st.button("🔄 Generate Schedule", key="generate_schedule_btn"):
    try:
        # VALIDATION CHECKS
        if not st.session_state['pets']:
            st.error("❌ Please add at least one pet...")
        elif not st.session_state['tasks']:
            st.error("❌ Please add at least one task...")
        else:
            # STEP 1: Create fresh Owner instance for scheduling
            schedule_owner = Owner(
                name=owner.name,
                email=owner.email,
                phone_number=owner.phone_number,
                occupation=owner.occupation,
                owner_id=owner.owner_id
            )
            
            # STEP 2: Assign pets from vault to schedule owner
            for pet in st.session_state['pets']:
                schedule_owner.add_pet(pet)  # Calls Owner.add_pet()
            
            # STEP 3: Assign tasks from vault to pets
            for i, task in enumerate(st.session_state['tasks']):
                pet_index = i % len(st.session_state['pets'])
                st.session_state['pets'][pet_index].add_task(task)  # Calls Pet.add_task()
            
            # STEP 4: Create Scheduler with constraints
            constraints = Constraints()
            constraints.set_city("San Francisco")
            # ... more constraint settings
            
            scheduler = Scheduler(schedule_owner, constraints)
            
            # STEP 5: Call Scheduler.generate_optimal_schedule()
            schedule = scheduler.generate_optimal_schedule("2025-03-29")
            
            # STEP 6: Store schedule in vault
            st.session_state['last_schedule'] = schedule
            
            # STEP 7: Show success
            st.success(f"✅ Schedule generated successfully! ...")
```

### Class Methods Called

#### 1. **Owner.add_pet(pet)**
Adds each pet from vault to the schedule owner.

#### 2. **Pet.add_task(task)** (pawpal_system.py)
```python
def add_task(self, task):
    """Adds a task to the pet's task list."""
    task.pet_id = self.pet_id  # Associate task with this pet
    if task not in self.tasks:
        self.tasks.append(task)
        return True
    return False
```

**What it does:** Associates a task with a specific pet (e.g., "Morning walk" belongs to "Mochi").

#### 3. **Scheduler.generate_optimal_schedule(date, constraints)** (pawpal_system.py)
```python
def generate_optimal_schedule(self, date, constraints=None):
    """
    Generates an optimal daily schedule for all pets.
    
    Returns: Schedule object with ordered, conflict-free events
    """
    # Gets all tasks from all pets
    all_tasks = self.owner.get_all_tasks()
    
    # Sorts by priority and time
    sorted_tasks = sorted(all_tasks, ...)
    
    # Creates ScheduleEvent objects and adds to schedule
    schedule = Schedule(date)
    for task in sorted_tasks:
        event = ScheduleEvent(...)
        schedule.add_event(event)  # Checks for conflicts
    
    return schedule
```

**What it does:** 
1. Gets all tasks from all pets via `owner.get_all_tasks()`
2. Sorts tasks by priority and time
3. Creates conflict-free schedule events
4. Returns Schedule object with ordered events

### Session State Update

```
st.session_state['last_schedule'] = schedule
    ↓
Vault now contains:
{
  'owner': Owner(...),
  'pets': [Mochi(tasks=[...])],
  'tasks': [...],
  'last_schedule': Schedule(
    events=[
      ScheduleEvent("Morning walk", start="08:00", end="08:20"),
      ScheduleEvent("Feeding", start="12:00", end="12:10"),
      ...
    ]
  )
}
```

### UI Update Flow

```
1. Button clicked
   ↓
2. Pets and tasks retrieved from vault
   ↓
3. Tasks assigned to pets (Pet.add_task())
   ↓
4. Scheduler.generate_optimal_schedule() called
   ↓
5. Schedule stored in vault (st.session_state['last_schedule'])
   ✅ Schedule PERSISTS - no need to regenerate!
   ↓
6. Schedule Display section (Lines 207-227) runs
   ↓
7. UI shows schedule events:
   "🕐 08:00 - 08:20 | 📌 Morning walk | ⭐ high"
   "🕐 12:00 - 12:10 | 📌 Feeding | ⭐ high"
   etc.
```

---

## 5. Architecture Summary: Form → Logic → Vault → Display

### Pattern 1: Simple Object Creation (Adding Pet/Task)

```
┌─────────────────────────────────────────────────────────┐
│ USER FORM (Streamlit UI)                                │
│ Owner enters: Pet name "Mochi", Species "dog"           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓ Button Click
┌─────────────────────────────────────────────────────────┐
│ CREATE OBJECT (Python class __init__)                   │
│ new_pet = Pet(name="Mochi", species="dog", ...)        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓ st.session_state['pets'].append()
┌─────────────────────────────────────────────────────────┐
│ CALL OWNER METHOD                                       │
│ owner.add_pet(new_pet)                                  │
│ → Updates owner.pets list                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓ st.rerun()
┌─────────────────────────────────────────────────────────┐
│ DISPLAY FROM VAULT (Streamlit renders)                  │
│ st.session_state['pets'] → "🐾 Mochi (dog)"            │
└─────────────────────────────────────────────────────────┘
```

### Pattern 2: Complex Orchestration (Generating Schedule)

```
┌─────────────────────────────────────────────────────────┐
│ RETRIEVE FROM VAULT                                     │
│ pets = st.session_state['pets']                         │
│ tasks = st.session_state['tasks']                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ CALL OWNER/PET METHODS                                  │
│ owner.add_pet() → Associates pets with owner            │
│ pet.add_task() → Associates tasks with pets             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ CALL SCHEDULER METHOD                                   │
│ scheduler.generate_optimal_schedule(...)                │
│ → Returns: Schedule with ordered, conflict-free events  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ STORE IN VAULT (Persistence!)                           │
│ st.session_state['last_schedule'] = schedule            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│ DISPLAY FROM VAULT                                      │
│ schedule.get_events() → Render timeline                 │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Key Methods Used

### Owner Methods (Pet Management)
| Method | Called From | Effect |
|--------|------------|--------|
| `add_pet(pet)` | Button "Add Pet" | Adds Pet to owner.pets list |
| `remove_pet(pet)` | Button "Delete" | Removes Pet from owner.pets list |
| `get_pets()` | Schedule generation | Returns all owner's pets |
| `get_all_tasks()` | Scheduler | Returns all tasks across all pets |

### Pet Methods (Task Management)
| Method | Called From | Effect |
|--------|------------|--------|
| `add_task(task)` | Schedule generation | Adds Task to pet.tasks list |
| `remove_task(task)` | (UI deletion button) | Removes Task from pet.tasks |
| `get_tasks()` | Display section | Returns all pet's tasks |
| `get_incomplete_tasks()` | Scheduler filtering | Returns uncompleted tasks |

### Task Methods (Status Management)
| Method | Called From | Effect |
|--------|------------|--------|
| `mark_complete()` | (Task completion button) | Sets completion_status = True |
| `mark_incomplete()` | (Task reset button) | Sets completion_status = False |
| `is_complete()` | Task display table | Returns completion status |

### Scheduler Methods (Orchestration)
| Method | Called From | Effect |
|--------|------------|--------|
| `generate_optimal_schedule(date, constraints)` | Button "Generate Schedule" | Creates Schedule with conflict-free events |
| `get_task_summary()` | (Display section) | Returns formatted task list |
| `get_suggestions()` | (Display section) | Returns optimization suggestions |

---

## 7. The Vault Pattern: How Data Persists

### Why Session State?

Streamlit reruns your code **every time** a user interacts:

```
User clicks button
    ↓
Script runs top-to-bottom
    ↓
All local variables are recreated (LOST!)
    ↓
st.session_state survives (PERSISTED!)
```

### Vault Initialization (Lines 13-30)

```python
if 'owner' not in st.session_state:
    st.session_state['owner'] = Owner(...)  # Created ONCE

if 'pets' not in st.session_state:
    st.session_state['pets'] = []  # Created ONCE

if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []  # Created ONCE

if 'last_schedule' not in st.session_state:
    st.session_state['last_schedule'] = None  # Created ONCE
```

### Accessing Vault Data

```python
owner = st.session_state['owner']        # Get owner from vault
new_pet = Pet(...)                       # Create new object
st.session_state['pets'].append(new_pet) # Add to vault
owner.add_pet(new_pet)                   # Update owner's internal list
```

### Vault Persistence

```
Rerun 1: User adds "Mochi"
  → st.session_state['pets'] = [Mochi]

Rerun 2: User clicks button
  → Script reruns
  → if 'pets' not in st.session_state: SKIPPED (already exists!)
  → st.session_state['pets'] = [Mochi]  ← Still there!
  
Rerun 3: User adds "Fluffy"
  → st.session_state['pets'] = [Mochi, Fluffy]  ← Persisted!
```

---

## 8. Error Handling & Validation

### Pet Addition Validation
```python
if st.button("➕ Add Pet", key="add_pet_btn"):
    if new_pet_name:  # ✅ Check: not empty
        # Create and add pet
    else:
        st.error("Please enter a pet name")  # ❌ Error message
```

### Schedule Generation Validation
```python
if st.button("🔄 Generate Schedule", key="generate_schedule_btn"):
    if not st.session_state['pets']:  # ✅ Check: has pets
        st.error("❌ Please add at least one pet...")
    elif not st.session_state['tasks']:  # ✅ Check: has tasks
        st.error("❌ Please add at least one task...")
    else:
        # Generate schedule
```

---

## 9. Complete Data Flow Example

### Scenario: User wants to add pet and generate schedule

```
STEP 1: Owner enters "Mochi" (name) + "dog" (species) + clicks "Add Pet"
  → Pet.__init__() creates Pet object
  → st.session_state['pets'].append(Mochi)
  → Owner.add_pet(Mochi) → owner.pets = [Mochi]
  → st.rerun()

STEP 2: Owner enters "Morning walk" + "20 min" + "high" + clicks "Add Task"
  → Task.__init__() creates Task object
  → st.session_state['tasks'].append(Task)
  → st.rerun()

STEP 3: Owner clicks "Generate Schedule"
  → Pets retrieved: [Mochi]
  → Tasks retrieved: [Morning walk]
  → Pet.add_task(Task) → Mochi.tasks = [Morning walk]
  → Scheduler.generate_optimal_schedule()
    → Gets all tasks via owner.get_all_tasks()
    → Sorts by priority
    → Creates conflict-free schedule
    → Returns Schedule object
  → st.session_state['last_schedule'] = schedule
  → st.rerun()

STEP 4: Display schedule
  → Schedule Display section reads from vault
  → Shows: "🕐 08:00 - 08:20 | 📌 Morning walk | ⭐ high"
  → Data PERSISTS - no regeneration needed!
```

---

## Summary

Your app is **fully wired**:

✅ **User Form** → Form inputs collected
✅ **Create Object** → Class constructors instantiate objects  
✅ **Call Method** → Owner/Pet methods update relationships
✅ **Store in Vault** → session_state persists data
✅ **Rerun Display** → st.rerun() refreshes UI
✅ **Display from Vault** → Data rendered back to user

The key insight: **Data flows OUT to the vault, gets processed by class methods, then flows BACK into the display.**
