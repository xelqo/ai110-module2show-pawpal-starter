# PawPal+ UI/Logic Integration Guide

## Overview

This document describes how the Streamlit user interface (`app.py`) is now connected to the pet care scheduling system (`pawpal_system.py`).

---

## Step 1: Import Statement ✅

**File:** `app.py` (Line 2)

```python
from pawpal_system import Owner, Pet, Task, Constraints, Scheduler
```

This single import statement brings five essential classes from the backend logic into the Streamlit app:

| Class | Purpose |
|-------|---------|
| **Owner** | Represents the pet owner with contact info, work schedule, and manages all pets |
| **Pet** | Represents a pet with species, age, weight, health needs, and task list |
| **Task** | Represents a single pet care activity with description, time, duration, and priority |
| **Constraints** | Defines environmental constraints (weather, location, available hours) |
| **Scheduler** | The "brain" that orchestrates tasks across all pets and generates schedules |

---

## Step 2: Data Flow Architecture

```
USER INTERFACE (app.py)
    ↓
    [Streamlit Input Form]
    ├─ Owner name
    ├─ Pet name & species
    └─ Task list (title, duration, priority)
    ↓
CONVERSION LAYER
    ├─ Create Owner instance
    ├─ Create Pet instance
    ├─ Create Task instances
    └─ Create Constraints instance
    ↓
BUSINESS LOGIC (pawpal_system.py)
    ├─ Owner manages Pets
    ├─ Pet stores Tasks
    └─ Scheduler orchestrates everything
    ↓
SCHEDULE GENERATION
    ├─ Sort tasks by priority & time
    ├─ Detect conflicts
    └─ Calculate durations
    ↓
DISPLAY RESULTS
    ├─ Task Summary
    ├─ Daily Schedule
    ├─ Schedule Metrics
    └─ System Suggestions
```

---

## Step 3: Implementation Details

### How the App Uses the Classes

#### 3.1 Creating an Owner
```python
owner = Owner(
    name=owner_name,                    # From: st.text_input()
    email="owner@example.com",
    phone_number="555-0000",
    occupation="Pet Owner",
    owner_id="owner_001"
)
```

#### 3.2 Creating a Pet
```python
pet = Pet(
    name=pet_name,                      # From: st.text_input()
    species=species,                    # From: st.selectbox()
    age=1,
    weight=50.0,
    pet_id="pet_001",
    daily_activity_minutes=60
)

# Add pet to owner (establishing relationship)
owner.add_pet(pet)
```

#### 3.3 Creating Tasks
```python
for task_data in st.session_state.tasks:  # From: user form inputs
    task = Task(
        description=task_data["title"],           # Task title
        time="09:00",                             # Default time
        frequency="daily",
        duration_minutes=task_data["duration_minutes"],  # Duration
        priority=task_data["priority"]            # Priority level
    )
    pet.add_task(task)  # Add task to pet
```

#### 3.4 Setting Up Constraints
```python
constraints = Constraints()
constraints.set_city("San Francisco")
constraints.set_climate("Temperate")
constraints.set_available_exercise_hours([("08:00", "20:00")])
constraints.set_weather_conditions(["Clear"])
constraints.set_has_yard(True)
```

#### 3.5 Generating the Schedule
```python
# Create the scheduler (the "brain")
scheduler = Scheduler(owner, constraints)

# Generate optimal schedule
schedule = scheduler.generate_optimal_schedule("2025-03-29")
```

---

## Step 4: Displaying Results

The app displays results in multiple sections:

### Task Summary
```python
st.markdown(scheduler.get_task_summary())
```
**Output:** Shows all tasks for each pet, with completion status

### Daily Schedule
```python
for event in sorted(schedule.get_events(), key=lambda e: e.start_time):
    # Display each scheduled event with time, name, and priority
```
**Output:** Chronological list of all scheduled tasks

### Metrics
```python
st.metric("Total Duration", f"{schedule.get_total_duration()} minutes")
st.metric("Wellbeing Score", f"{schedule.get_wellbeing_score():.2f}/1.0")
```
**Output:** Key performance indicators

### System Suggestions
```python
suggestions = scheduler.get_suggestions()
for suggestion in suggestions:
    st.info(suggestion)
```
**Output:** AI-generated recommendations for optimization

---

## Step 5: Error Handling

The app includes validation and error handling:

```python
if not owner_name:
    st.error("Please enter an owner name.")
elif not pet_name:
    st.error("Please enter a pet name.")
elif not st.session_state.tasks:
    st.error("Please add at least one task.")
else:
    # Try to create schedule
    try:
        # ... scheduling logic ...
    except Exception as e:
        st.error(f"Error generating schedule: {str(e)}")
```

---

## Class Relationships

```
Owner (the container)
  └── has_many: Pet
        └── Pet
              └── has_many: Task
                    └── Task (with priority, time, duration)

Scheduler (the orchestrator)
  ├── manages: Owner (gets all pets and tasks from here)
  ├── manages: Constraints
  ├── creates: Schedule
  └── generates: ScheduleEvents (from Tasks)
```

---

## Data Transformation Example

### Before (UI Input)
```
Owner: "Jordan"
Pet: "Mochi" (cat)
Tasks:
  - "Morning walk" (20 min, high)
  - "Breakfast" (10 min, high)
  - "Playtime" (15 min, medium)
```

### After (Backend Objects)
```python
owner = Owner(name="Jordan", ...)
pet = Pet(name="Mochi", species="cat", ...)
owner.add_pet(pet)

task1 = Task(description="Morning walk", duration_minutes=20, priority="high")
task2 = Task(description="Breakfast", duration_minutes=10, priority="high")
task3 = Task(description="Playtime", duration_minutes=15, priority="medium")

pet.add_task(task1)
pet.add_task(task2)
pet.add_task(task3)
```

### Generated Output (Schedule)
```
09:00 - 09:20: Morning walk [high]
09:20 - 09:30: Breakfast [high]
09:30 - 09:45: Playtime [medium]

Total Duration: 45 minutes
Wellbeing Score: 0.67/1.0
Suggestions: 15 more minutes of exercise needed
```

---

## Testing the Integration

To verify the integration works:

```bash
# Test 1: Verify imports work
python3 -c "from pawpal_system import Owner, Pet, Task, Constraints, Scheduler; print('✅ Imports OK')"

# Test 2: Run the main.py testing script
python3 main.py

# Test 3: Run unit tests
python3 -m pytest tests/test_pawpal.py -v

# Test 4: Run the Streamlit app
streamlit run app.py
```

---

## Next Steps for Enhancement

Once the basic integration is working, consider:

1. **Persistent Storage** - Save owner/pet/task data to JSON or database
2. **Task Time Customization** - Let users set custom times for each task
3. **Multi-Pet Support** - Allow adding multiple pets in the UI
4. **Schedule Export** - Download schedule as CSV/PDF
5. **Optimization Options** - Let users choose optimization criteria (wellbeing vs. owner availability)
6. **Task History** - Track completed tasks over time
7. **Recurring Tasks** - Support weekly/monthly task patterns

---

## Summary

The **bridge between UI and logic** is now established:

✅ Import statement brings classes into app.py  
✅ UI inputs are converted to class instances  
✅ Scheduler generates optimized schedule  
✅ Results are displayed back to user  
✅ Error handling ensures robust operation  

The system is now **fully functional** and ready for user interaction! 🐾
