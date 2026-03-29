# UI Components & Method Mapping Reference

This document shows **exactly which class methods are called** by each UI component in `app.py`.

---

## 1. Owner Information Section

### UI Location
Lines 60-66 of `app.py`

### Code
```python
owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
if owner_name != owner.name:
    owner.name = owner_name
    st.success(f"✅ Owner updated: {owner.name}")
```

### Methods Called
- ✅ **None** - directly modifying `owner.name` attribute

### Data Flow
```
User input → owner.name = new_value → Display success
```

### Session State
- Reads: `st.session_state['owner']` 
- Modifies: Direct property assignment (not calling a method)
- Persists: Yes (owner object in vault)

---

## 2. Add Pets Section

### UI Location
Lines 72-92 of `app.py`

### Code
```python
if st.button("➕ Add Pet", key="add_pet_btn"):
    if new_pet_name:
        new_pet = Pet(
            name=new_pet_name,
            species=new_pet_species,
            age=1,
            weight=50.0,
            pet_id=f"pet_{len(st.session_state['pets']) + 1}",
            daily_activity_minutes=60
        )
        st.session_state['pets'].append(new_pet)
        owner.add_pet(new_pet)
        st.success(f"✅ {new_pet_name} the {new_pet_species} added!")
        st.rerun()
```

### Methods Called

#### 1. **Pet.__init__()** 
```python
class Pet:
    def __init__(self, name, species, age, weight, pet_id, daily_activity_minutes):
        # Constructor - creates Pet object
```
- **Location:** `pawpal_system.py` (Constructor)
- **What it does:** Initializes new Pet with properties
- **Returns:** Pet object
- **Side effects:** Creates empty `self.tasks = []`

#### 2. **Owner.add_pet(pet)**
```python
class Owner:
    def add_pet(self, pet):
        """Adds a pet to the owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)
            return True
        return False
```
- **Location:** `pawpal_system.py` (~line 400)
- **What it does:** Adds pet to owner's internal pet list
- **Returns:** Boolean (True if added, False if already exists)
- **Side effects:** Updates `owner.pets` list

### Data Flow
```
User submits form
    ↓
Pet.__init__() creates object
    ↓
st.session_state['pets'].append(new_pet)  [Vault]
    ↓
owner.add_pet(new_pet)  [Owner's internal list]
    ↓
st.rerun()  [Refresh display]
    ↓
Display updated with new pet
```

### Session State
- Reads: `st.session_state['pets']` (to get count)
- Modifies: 
  - Appends to `st.session_state['pets']`
  - Updates `st.session_state['owner'].pets` via `add_pet()`
- Persists: Yes

### Display Update Section
```python
if st.session_state['pets']:
    st.write("**Your Pets (stored in vault):**")
    for i, pet in enumerate(st.session_state['pets']):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"🐾 **{pet.name}** ({pet.species})")
        with col2:
            st.caption(f"Tasks: {len(pet.get_tasks())}")
        with col3:
            if st.button("🗑️", key=f"delete_pet_{i}"):
                st.session_state['pets'].pop(i)
                owner.remove_pet(pet)
                st.success("Pet removed!")
                st.rerun()
```

### Methods Called in Display

#### 3. **Pet.get_tasks()**
```python
class Pet:
    def get_tasks(self):
        """Returns the list of tasks for this pet."""
        return self.tasks
```
- **Location:** `pawpal_system.py` (~line 250)
- **What it does:** Returns pet's task list
- **Returns:** List of Task objects
- **Used for:** `len(pet.get_tasks())` - displays task count

#### 4. **Owner.remove_pet(pet)**
```python
class Owner:
    def remove_pet(self, pet):
        """Removes a pet from the owner's pet list."""
        if pet in self.pets:
            self.pets.remove(pet)
            return True
        return False
```
- **Location:** `pawpal_system.py` (~line 410)
- **What it does:** Removes pet from owner's pet list
- **Returns:** Boolean (True if removed, False if not found)
- **Side effects:** Updates `owner.pets` list

---

## 3. Add Tasks Section

### UI Location
Lines 116-145 of `app.py`

### Code
```python
if st.button("➕ Add Task", key="add_task_btn"):
    if task_title:
        task = Task(
            description=task_title,
            time="09:00",
            frequency="daily",
            duration_minutes=int(duration),
            priority=priority
        )
        st.session_state['tasks'].append(task)
        st.success(f"✅ Task '{task_title}' added to vault!")
        st.rerun()
```

### Methods Called

#### 1. **Task.__init__()**
```python
class Task:
    def __init__(self, description, time, frequency, duration_minutes, priority):
        self.description = description
        self.time = time
        self.frequency = frequency
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.completion_status = False
```
- **Location:** `pawpal_system.py` (Constructor)
- **What it does:** Creates new Task object
- **Returns:** Task object
- **Side effects:** Sets `completion_status = False` by default

### Data Flow
```
User submits task form
    ↓
Task.__init__() creates object
    ↓
st.session_state['tasks'].append(task)  [Vault]
    ↓
st.rerun()  [Refresh display]
    ↓
Display updated with new task
```

### Session State
- Reads: None
- Modifies: Appends to `st.session_state['tasks']`
- Persists: Yes

### Display Update Section
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
    
    if st.button("🗑️ Clear All Tasks", key="clear_tasks_btn"):
        st.session_state['tasks'].clear()
        st.success("All tasks cleared!")
        st.rerun()
```

### Methods Called in Display

#### 2. **Task.is_complete()**
```python
class Task:
    def is_complete(self):
        """Returns True if task is marked complete."""
        return self.completion_status
```
- **Location:** `pawpal_system.py` (~line 150)
- **What it does:** Returns task completion status
- **Returns:** Boolean
- **Used for:** Display "✓" or "○" in task table

---

## 4. Build Schedule Section

### UI Location
Lines 167-205 of `app.py`

### Code
```python
if st.button("🔄 Generate Schedule", key="generate_schedule_btn"):
    try:
        if not st.session_state['pets']:
            st.error("❌ Please add at least one pet...")
        elif not st.session_state['tasks']:
            st.error("❌ Please add at least one task...")
        else:
            # Create fresh owner for scheduling
            schedule_owner = Owner(
                name=owner.name,
                email=owner.email,
                phone_number=owner.phone_number,
                occupation=owner.occupation,
                owner_id=owner.owner_id
            )
            
            # Add pets to schedule owner
            for pet in st.session_state['pets']:
                schedule_owner.add_pet(pet)
            
            # Assign tasks to pets
            for i, task in enumerate(st.session_state['tasks']):
                pet_index = i % len(st.session_state['pets'])
                st.session_state['pets'][pet_index].add_task(task)
            
            # Create scheduler
            constraints = Constraints()
            constraints.set_city("San Francisco")
            constraints.set_climate("Temperate")
            constraints.set_available_exercise_hours([("08:00", "20:00")])
            constraints.set_weather_conditions(["Clear"])
            constraints.set_has_yard(True)
            
            scheduler = Scheduler(schedule_owner, constraints)
            
            # Generate schedule
            schedule = scheduler.generate_optimal_schedule("2025-03-29")
            
            # Store in vault
            st.session_state['last_schedule'] = schedule
            st.success(f"✅ Schedule generated successfully! ...")
```

### Methods Called

#### 1. **Owner.__init__()**
```python
class Owner:
    def __init__(self, name, email, phone_number, occupation, owner_id):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.occupation = occupation
        self.owner_id = owner_id
        self.pets = []
```
- **Purpose:** Create fresh owner instance for scheduling
- **Why fresh?** Ensures clean state for schedule generation

#### 2. **Owner.add_pet(pet)** (Called in loop)
```python
for pet in st.session_state['pets']:
    schedule_owner.add_pet(pet)
```
- **Purpose:** Associate all pets from vault with schedule owner
- **Result:** `schedule_owner.pets` now contains all pets

#### 3. **Pet.add_task(task)** (Called in loop)
```python
for i, task in enumerate(st.session_state['tasks']):
    pet_index = i % len(st.session_state['pets'])
    st.session_state['pets'][pet_index].add_task(task)
```
- **Location:** `pawpal_system.py` (~line 250)
- **Code:**
```python
def add_task(self, task):
    """Adds a task to the pet's task list."""
    task.pet_id = self.pet_id
    if task not in self.tasks:
        self.tasks.append(task)
        return True
    return False
```
- **What it does:** Assigns task to specific pet
- **Side effects:** Sets `task.pet_id` to associate task with pet
- **How assignment works:** Cycle through pets if more tasks than pets (modulo logic)

#### 4. **Constraints Methods**
```python
constraints = Constraints()
constraints.set_city("San Francisco")
constraints.set_climate("Temperate")
constraints.set_available_exercise_hours([("08:00", "20:00")])
constraints.set_weather_conditions(["Clear"])
constraints.set_has_yard(True)
```
- **Location:** `pawpal_system.py` (~line 600)
- **What they do:** Set environmental constraints for scheduling
- **Example:**
```python
def set_city(self, city):
    self.city = city
```

#### 5. **Scheduler.__init__()**
```python
scheduler = Scheduler(schedule_owner, constraints)
```
- **Location:** `pawpal_system.py` (~line 700)
- **Code:**
```python
class Scheduler:
    def __init__(self, owner, constraints=None):
        self.owner = owner
        self.constraints = constraints
```
- **What it does:** Creates scheduler with owner and constraints

#### 6. **Scheduler.generate_optimal_schedule(date)**
```python
schedule = scheduler.generate_optimal_schedule("2025-03-29")
```
- **Location:** `pawpal_system.py` (~line 750)
- **Code:**
```python
def generate_optimal_schedule(self, date, constraints=None):
    """
    Generates an optimal daily schedule for all pets.
    
    Steps:
    1. Get all tasks from all pets
    2. Sort by priority and time
    3. Create conflict-free events
    4. Return Schedule object
    """
    all_tasks = self.owner.get_all_tasks()
    sorted_tasks = sorted(all_tasks, key=lambda t: (priority_order[t.priority], t.time))
    
    schedule = Schedule(date)
    for task in sorted_tasks:
        event = ScheduleEvent(...)
        schedule.add_event(event)
    
    return schedule
```
- **What it does:** Core orchestration - builds daily schedule
- **Returns:** Schedule object with ordered events
- **Calls internally:**
  - `Owner.get_all_tasks()` - gets all tasks from all pets
  - `Schedule.add_event()` - adds event to schedule (checks conflicts)

### Data Flow
```
User clicks "Generate Schedule"
    ↓
Validate pets and tasks exist
    ↓
Owner.__init__() creates fresh owner
    ↓
Owner.add_pet() (loop) - associate pets
    ↓
Pet.add_task() (loop) - assign tasks to pets
    ↓
Constraints.set_*() - configure environment
    ↓
Scheduler.__init__() - create orchestrator
    ↓
Scheduler.generate_optimal_schedule() - build schedule
  ├─ Owner.get_all_tasks() (inside)
  ├─ Schedule.add_event() (inside, multiple times)
  └─ Returns Schedule object
    ↓
st.session_state['last_schedule'] = schedule [Vault]
    ↓
st.success() displays confirmation
```

### Session State
- Reads: `st.session_state['pets']`, `st.session_state['tasks']`
- Modifies: Assigns tasks to pets (updates vault pet objects)
- Stores: `st.session_state['last_schedule'] = schedule`
- Persists: Yes

---

## 5. Schedule Display Section

### UI Location
Lines 207-227 of `app.py`

### Code
```python
st.subheader("📅 Schedule Display")

if st.session_state['last_schedule'] is not None:
    schedule = st.session_state['last_schedule']
    
    if schedule.get_events():
        st.info(f"✅ Schedule contains {len(schedule.get_events())} events")
        
        for event in sorted(schedule.get_events(), key=lambda e: e.start_time):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.text(f"🕐 {event.start_time} - {event.end_time}")
            with col2:
                st.text(f"📌 {event.task_name}")
            with col3:
                st.text(f"⭐ {event.priority}")
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Duration", f"{schedule.get_total_duration()} min")
        with col2:
            st.metric("Wellbeing Score", f"{schedule.get_wellbeing_score():.2f}/1.0")
    else:
        st.info("Schedule generated but contains no events.")
else:
    st.info("👆 Generate a schedule above...")
```

### Methods Called

#### 1. **Schedule.get_events()**
```python
class Schedule:
    def get_events(self):
        """Returns list of all scheduled events."""
        return self.events
```
- **What it does:** Returns all ScheduleEvent objects in schedule
- **Returns:** List of events
- **Used for:** Display and metrics calculation

#### 2. **Schedule.get_total_duration()**
```python
class Schedule:
    def get_total_duration(self):
        """Returns total minutes across all events."""
        return sum(event.get_duration() for event in self.events)
```
- **What it does:** Calculates total schedule duration
- **Returns:** Integer (minutes)
- **Calls internally:** `ScheduleEvent.get_duration()`

#### 3. **Schedule.get_wellbeing_score()**
```python
class Schedule:
    def get_wellbeing_score(self):
        """Returns schedule quality metric (0-1)."""
        # Complex calculation based on event distribution
```
- **What it does:** Evaluates schedule quality
- **Returns:** Float (0.0 to 1.0)

#### 4. **ScheduleEvent.get_duration()**
```python
class ScheduleEvent:
    def get_duration(self):
        """Returns duration in minutes between start and end times."""
        start = datetime.strptime(self.start_time, "%H:%M")
        end = datetime.strptime(self.end_time, "%H:%M")
        return int((end - start).total_seconds() / 60)
```
- **What it does:** Calculates event duration
- **Returns:** Integer (minutes)

### Data Flow
```
Schedule Display section executes (every rerun)
    ↓
Check if st.session_state['last_schedule'] exists
    ↓
If yes:
  ├─ Schedule.get_events() → display all events
  ├─ Schedule.get_total_duration() → show metric
  ├─ Schedule.get_wellbeing_score() → show metric
  └─ Events sorted and rendered
    ↓
If no:
  └─ Show "Generate schedule above" message
```

### Session State
- Reads: `st.session_state['last_schedule']`
- Modifies: None
- Persists: Yes (displays stored schedule without regenerating)

---

## Summary Table: All Methods by Action

| User Action | UI Line | Class Method | What It Does |
|-------------|---------|--------------|-------------|
| Change owner name | 64 | Direct assignment | Set `owner.name` |
| Click "Add Pet" | 78 | `Pet.__init__()` | Create Pet object |
| | 84 | `Owner.add_pet(pet)` | Add to owner's list |
| Click delete pet | 105 | `Owner.remove_pet(pet)` | Remove from list |
| Display pet | 102 | `Pet.get_tasks()` | Get task count |
| Click "Add Task" | 116 | `Task.__init__()` | Create Task object |
| Display tasks | 150 | `Task.is_complete()` | Get status |
| Click "Generate" | 177 | `Owner.__init__()` | Create schedule owner |
| | 183 | `Owner.add_pet(pet)` | Associate pets |
| | 188 | `Pet.add_task(task)` | Assign task to pet |
| | 194 | `Constraints.set_*()` | Configure limits |
| | 197 | `Scheduler.__init__()` | Create orchestrator |
| | 200 | `Scheduler.generate_optimal_schedule()` | Build schedule |
| Display schedule | 213 | `Schedule.get_events()` | Get event list |
| | 223 | `Schedule.get_total_duration()` | Calculate duration |
| | 226 | `Schedule.get_wellbeing_score()` | Calculate score |

---

## Key Insights

### 1. Vault Synchronization
```python
# When adding pet:
st.session_state['pets'].append(new_pet)   # Vault
owner.add_pet(new_pet)                      # Owner's list

# Both must be updated!
```

### 2. Object Creation Happens in UI
```python
# UI creates the object (not pawpal_system)
new_pet = Pet(...)  # ← UI does this
owner.add_pet(new_pet)  # ← pawpal_system adds it
```

### 3. Methods Do Relationship Management
```python
# Constructor: creates object
Pet.__init__()

# Methods: manage relationships
Owner.add_pet()      # links owner to pet
Pet.add_task()       # links pet to task
Scheduler.generate_optimal_schedule()  # uses relationships
```

### 4. Rerun Updates Display
```python
# Method modifies data
owner.add_pet(pet)
st.session_state['pets'].append(pet)

# st.rerun() reruns display section
st.rerun()

# Display now shows new data
for pet in st.session_state['pets']:
    st.write(pet)  # ← NEW pet included
```

---

## For Developers: Common Patterns

### Pattern 1: Create → Add to Vault → Call Method → Rerun

```python
new_obj = Class(...)                          # Create
st.session_state['key'].append(new_obj)       # Vault
parent.add_child(new_obj)                     # Sync
st.rerun()                                    # Display
```

### Pattern 2: Remove from Vault → Call Method → Rerun

```python
st.session_state['key'].pop(index)            # Vault
parent.remove_child(obj)                      # Sync
st.rerun()                                    # Display
```

### Pattern 3: Retrieve → Process → Store → Display

```python
data = st.session_state['key']                # Retrieve
result = complex_method(data)                 # Process
st.session_state['store_key'] = result        # Store
st.write(result)                              # Display
```
