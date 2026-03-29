# St.session_state Investigation & Implementation Guide

## What is st.session_state?

`st.session_state` is **a persistent dictionary** that survives between app reruns. It's the solution to Streamlit's stateless nature.

### The Problem
Streamlit runs your script from top to bottom every time:
- User clicks a button → Script reruns
- User types in a text box → Script reruns
- User refreshes the page → Script reruns

If you create an `Owner` object at the top level, it gets recreated (empty) on every rerun.

### The Solution
Use `st.session_state` to store objects that should persist:

```python
# Check if Owner exists in the vault
if 'owner' not in st.session_state:
    # If not, create it (only runs once)
    st.session_state['owner'] = Owner(name="Jordan", ...)

# Now access it (persists across reruns)
current_owner = st.session_state['owner']
```

---

## How st.session_state Works

Think of it as a dictionary with special persistence:

```python
# Check if key exists (using 'in' operator)
if 'owner' not in st.session_state:
    st.session_state['owner'] = Owner(...)

# Access using dictionary syntax
owner = st.session_state['owner']
owner.name = "New Name"

# OR access using attribute syntax
owner = st.session_state.owner
owner.name = "New Name"

# Both work identically!
```

### Key Patterns

| Pattern | Syntax | Purpose |
|---------|--------|---------|
| **Check existence** | `'key' not in st.session_state` | Before creating |
| **Store value** | `st.session_state['key'] = value` | Save to persistent vault |
| **Read value** | `st.session_state['key']` | Get from vault |
| **Delete value** | `del st.session_state['key']` | Remove from vault |
| **List all keys** | `st.session_state.keys()` | See what's stored |

---

## Persistence Scope

✅ **Persists across:**
- Button clicks
- Text input changes
- Widget interactions
- App reruns triggered by user actions

❌ **Does NOT persist across:**
- Page refresh (F5)
- Browser tab close
- New browser session
- WebSocket connection reset

---

## Implementation Pattern for PawPal

### Pattern 1: Initialize Owner Once

```python
import streamlit as st
from pawpal_system import Owner, Pet, Task, Constraints, Scheduler

# At the top of your app, initialize the Owner object ONCE
if 'owner' not in st.session_state:
    st.session_state['owner'] = Owner(
        name="Default Owner",
        email="owner@example.com",
        phone_number="555-0000",
        occupation="Pet Owner",
        owner_id="owner_001"
    )

# Now you can safely use it throughout the app
owner = st.session_state['owner']

# User input to update owner
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name
```

### Pattern 2: Persistent Pet List

```python
# Initialize empty pet list
if 'pets' not in st.session_state:
    st.session_state['pets'] = []

# Add pets
if st.button("Add Pet"):
    new_pet = Pet(name="Mochi", species="cat", ...)
    st.session_state['pets'].append(new_pet)
    owner.add_pet(new_pet)

# Access pets anytime
for pet in st.session_state['pets']:
    st.write(f"Pet: {pet.name}")
```

### Pattern 3: Persistent Task List

```python
# Initialize empty task list
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

# Add tasks from form
if st.button("Add task"):
    task = Task(
        description=task_title,
        duration_minutes=duration,
        priority=priority,
        ...
    )
    st.session_state['tasks'].append(task)

# Display all tasks
st.write("Current tasks:")
for task in st.session_state['tasks']:
    st.write(f"• {task.description} ({task.duration_minutes} min)")
```

### Pattern 4: Persistent Schedule

```python
# Initialize schedule as None
if 'last_schedule' not in st.session_state:
    st.session_state['last_schedule'] = None

# Generate and store schedule
if st.button("Generate schedule"):
    scheduler = Scheduler(owner, constraints)
    schedule = scheduler.generate_optimal_schedule("2025-03-29")
    st.session_state['last_schedule'] = schedule

# Display stored schedule
if st.session_state['last_schedule']:
    st.write("Last generated schedule:")
    for event in st.session_state['last_schedule'].get_events():
        st.write(f"{event.start_time}: {event.task_name}")
```

---

## Complete App Structure with session_state

```python
import streamlit as st
from pawpal_system import Owner, Pet, Task, Constraints, Scheduler

st.title("🐾 PawPal+")

# ============================================================================
# STEP 1: INITIALIZE SESSION STATE (runs once per user session)
# ============================================================================

if 'owner' not in st.session_state:
    st.session_state['owner'] = Owner(
        name="Default Owner",
        email="owner@example.com",
        phone_number="555-0000",
        occupation="Pet Owner",
        owner_id="owner_001"
    )

if 'pets' not in st.session_state:
    st.session_state['pets'] = []

if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

if 'last_schedule' not in st.session_state:
    st.session_state['last_schedule'] = None

# ============================================================================
# STEP 2: GET REFERENCES (can use throughout app)
# ============================================================================

owner = st.session_state['owner']
pets = st.session_state['pets']
tasks = st.session_state['tasks']

# ============================================================================
# STEP 3: UI FOR OWNER INPUT
# ============================================================================

st.subheader("Owner Information")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name
    st.success(f"Owner name updated to: {owner.name}")

# ============================================================================
# STEP 4: UI FOR ADDING PETS
# ============================================================================

st.subheader("Add Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    if pet_name:
        new_pet = Pet(
            name=pet_name,
            species=species,
            age=1,
            weight=50.0,
            pet_id=f"pet_{len(st.session_state['pets']) + 1}"
        )
        st.session_state['pets'].append(new_pet)
        owner.add_pet(new_pet)
        st.success(f"✅ {pet_name} added!")
    else:
        st.error("Please enter a pet name")

# Display current pets
if st.session_state['pets']:
    st.write("**Current Pets:**")
    for pet in st.session_state['pets']:
        st.write(f"🐾 {pet.name} ({pet.species})")

# ============================================================================
# STEP 5: UI FOR ADDING TASKS
# ============================================================================

st.subheader("Add Tasks")
task_title = st.text_input("Task title", value="Morning walk")
duration = st.number_input("Duration (minutes)", value=20)
priority = st.selectbox("Priority", ["low", "medium", "high"])

if st.button("Add Task"):
    task = Task(
        description=task_title,
        time="09:00",
        frequency="daily",
        duration_minutes=int(duration),
        priority=priority
    )
    st.session_state['tasks'].append(task)
    st.success(f"✅ Task '{task_title}' added!")

# Display current tasks
if st.session_state['tasks']:
    st.write("**Current Tasks:**")
    for task in st.session_state['tasks']:
        st.write(f"• {task.description} ({task.duration_minutes} min, {task.priority})")

# ============================================================================
# STEP 6: GENERATE SCHEDULE (stores in session_state)
# ============================================================================

if st.button("Generate Schedule"):
    if not st.session_state['pets']:
        st.error("Please add at least one pet")
    elif not st.session_state['tasks']:
        st.error("Please add at least one task")
    else:
        try:
            # Add tasks to pets
            for pet in st.session_state['pets']:
                for task in st.session_state['tasks']:
                    pet.add_task(task)
            
            # Create constraints
            constraints = Constraints()
            constraints.set_city("San Francisco")
            constraints.set_climate("Temperate")
            constraints.set_available_exercise_hours([("08:00", "20:00")])
            constraints.set_weather_conditions(["Clear"])
            constraints.set_has_yard(True)
            
            # Generate schedule
            scheduler = Scheduler(owner, constraints)
            schedule = scheduler.generate_optimal_schedule("2025-03-29")
            
            # Store schedule in session_state
            st.session_state['last_schedule'] = schedule
            
            st.success("✅ Schedule generated!")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ============================================================================
# STEP 7: DISPLAY STORED SCHEDULE
# ============================================================================

if st.session_state['last_schedule']:
    st.subheader("📅 Generated Schedule")
    schedule = st.session_state['last_schedule']
    
    for event in sorted(schedule.get_events(), key=lambda e: e.start_time):
        st.write(f"🕐 {event.start_time}: {event.task_name} [{event.priority}]")
    
    st.metric("Total Duration", f"{schedule.get_total_duration()} min")
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Creating Object Every Rerun
❌ **Bad:**
```python
owner = Owner(name="Jordan", ...)  # Created on every rerun!
```

✅ **Good:**
```python
if 'owner' not in st.session_state:
    st.session_state['owner'] = Owner(name="Jordan", ...)
owner = st.session_state['owner']
```

### Pitfall 2: Not Checking Before Accessing
❌ **Bad:**
```python
owner = st.session_state['owner']  # Will crash if not initialized!
```

✅ **Good:**
```python
if 'owner' not in st.session_state:
    st.session_state['owner'] = Owner(...)
owner = st.session_state['owner']
```

### Pitfall 3: Forgetting to Update session_state After Changes
❌ **Bad:**
```python
owner.name = "New Name"  # Change made, but not persisted
```

✅ **Good:**
```python
owner = st.session_state['owner']
owner.name = "New Name"  # Change is automatically persisted
```

### Pitfall 4: Overwriting Objects
❌ **Bad:**
```python
st.session_state['owner'] = Owner(...)  # Creates new owner every time!
```

✅ **Good:**
```python
if 'owner' not in st.session_state:
    st.session_state['owner'] = Owner(...)
# Then modify as needed, don't recreate
```

---

## Debugging session_state

### View All Stored Data
```python
# Show what's in session_state
st.write("Session State Contents:")
st.write(st.session_state)
```

### Check What Keys Exist
```python
st.write("Keys in session_state:")
st.write(list(st.session_state.keys()))
```

### Clear Everything (for development)
```python
if st.button("Clear All Data"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.success("Cleared!")
```

---

## Implementation Checklist

- [ ] Add `if 'owner' not in st.session_state:` check at app start
- [ ] Initialize `Owner` object in session_state
- [ ] Add `if 'pets' not in st.session_state:` for pets list
- [ ] Add `if 'tasks' not in st.session_state:` for tasks list
- [ ] Add `if 'last_schedule' not in st.session_state:` for schedule
- [ ] Use `st.session_state['key']` to access objects throughout app
- [ ] Test that objects persist when clicking buttons
- [ ] Verify data survives across multiple button clicks
- [ ] Add debug display (`st.write(st.session_state)`) to verify

---

## Key Takeaway

```
st.session_state = Dictionary that survives reruns

Pattern:
if 'key' not in st.session_state:
    st.session_state['key'] = initial_value

# Then use it anywhere:
value = st.session_state['key']
value.do_something()
```

This transforms Streamlit from stateless to stateful! 🎉
