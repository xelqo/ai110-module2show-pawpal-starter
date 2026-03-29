import streamlit as st
from pawpal_system import Owner, Pet, Task, Constraints, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")
st.markdown("**Your Intelligent Pet Care Planning Assistant**")

# ============================================================================
# INITIALIZE SESSION STATE (Persistent Vault)
# ============================================================================

if 'owner' not in st.session_state:
    st.session_state['owner'] = Owner(
        name="Jordan",
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

if 'scheduler' not in st.session_state:
    st.session_state['scheduler'] = None

owner = st.session_state['owner']

with st.expander("ℹ️ About PawPal+", expanded=False):
    st.markdown(
        """
**PawPal+** is an intelligent pet care planning assistant that helps busy pet owners:
- Track and organize pet care tasks
- Generate optimized daily schedules
- Detect scheduling conflicts
- Filter and sort tasks intelligently
- Monitor pet wellbeing

Your data is saved automatically in the session (persists as you navigate).
"""
    )

st.divider()

# ============================================================================
# OWNER & PET MANAGEMENT
# ============================================================================

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("👤 Owner Information")
    owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
    if owner_name != owner.name:
        owner.name = owner_name

with col2:
    st.subheader("🐾 Add Pets")
    col_name, col_species = st.columns(2)
    with col_name:
        new_pet_name = st.text_input("Pet name", placeholder="e.g., Mochi", key="pet_name")
    with col_species:
        new_pet_species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"], key="pet_species")
    
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
        else:
            st.error("Please enter a pet name")

# Display current pets
if st.session_state['pets']:
    st.write("**Your Pets:**")
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
                st.rerun()
else:
    st.info("No pets yet. Add one above!")

st.divider()

# ============================================================================
# TASK MANAGEMENT
# ============================================================================

st.subheader("📋 Task Management")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", placeholder="e.g., Morning walk", key="task_input")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30, key="duration_input")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority_select")

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
        st.success(f"✅ Task '{task_title}' added!")
        st.rerun()
    else:
        st.error("Please enter a task title")

# Display tasks
if st.session_state['tasks']:
    st.write("**Tasks in Queue:**")
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
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ============================================================================
# SCHEDULE GENERATION
# ============================================================================

st.subheader("🕐 Generate Schedule")

if st.button("🔄 Generate Optimized Schedule", key="generate_schedule_btn"):
    try:
        if not st.session_state['pets']:
            st.error("❌ Please add at least one pet")
        elif not st.session_state['tasks']:
            st.error("❌ Please add at least one task")
        else:
            schedule_owner = Owner(
                name=owner.name,
                email=owner.email,
                phone_number=owner.phone_number,
                occupation=owner.occupation,
                owner_id=owner.owner_id
            )
            
            for pet in st.session_state['pets']:
                schedule_owner.add_pet(pet)
            
            for i, task in enumerate(st.session_state['tasks']):
                pet_index = i % len(st.session_state['pets'])
                st.session_state['pets'][pet_index].add_task(task)
            
            constraints = Constraints()
            constraints.set_city("San Francisco")
            constraints.set_climate("Temperate")
            constraints.set_available_exercise_hours([("08:00", "20:00")])
            constraints.set_weather_conditions(["Clear"])
            constraints.set_has_yard(True)
            
            scheduler = Scheduler(schedule_owner, constraints)
            schedule = scheduler.generate_optimal_schedule("2025-03-29")
            
            st.session_state['last_schedule'] = schedule
            st.session_state['scheduler'] = scheduler
            st.success(f"✅ Schedule generated! {len(schedule.get_events())} events scheduled")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.divider()

# ============================================================================
# SMART FEATURES
# ============================================================================

if st.session_state.get('scheduler') and st.session_state['pets']:
    scheduler = st.session_state['scheduler']
    
    st.subheader("🧠 Smart Algorithm Features")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Sort by Time", "✓ Filter Status", "🐾 Filter Pet", "⚠️ Conflicts"])
    
    # Tab 1: Sort by Time
    with tab1:
        sorted_tasks = scheduler.sort_tasks_by_time()
        if sorted_tasks:
            st.write("**Tasks arranged chronologically:**")
            task_data = {
                "Time": [t.time for t in sorted_tasks],
                "Task": [t.description for t in sorted_tasks],
                "Duration (min)": [t.duration_minutes for t in sorted_tasks],
                "Priority": [t.priority for t in sorted_tasks]
            }
            st.table(task_data)
        else:
            st.info("No tasks to sort")
    
    # Tab 2: Filter by Status
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            incomplete = scheduler.filter_tasks_by_status(completed=False)
            st.write(f"**Incomplete Tasks ({len(incomplete)})**")
            if incomplete:
                incomplete_data = {
                    "Task": [t.description for t in incomplete],
                    "Time": [t.time for t in incomplete],
                    "Priority": [t.priority for t in incomplete]
                }
                st.table(incomplete_data)
            else:
                st.success("✅ All tasks complete!")
        
        with col2:
            completed = scheduler.filter_tasks_by_status(completed=True)
            st.write(f"**Completed Tasks ({len(completed)})**")
            if completed:
                completed_data = {
                    "Task": [t.description for t in completed],
                    "Time": [t.time for t in completed]
                }
                st.table(completed_data)
            else:
                st.info("No completed tasks yet")
    
    # Tab 3: Filter by Pet
    with tab3:
        for pet in st.session_state['pets']:
            with st.expander(f"🐾 {pet.name} ({pet.species.capitalize()})", expanded=True):
                pet_tasks = scheduler.filter_tasks_by_pet(pet.name)
                if pet_tasks:
                    pet_data = {
                        "Task": [t.description for t in pet_tasks],
                        "Time": [t.time for t in pet_tasks],
                        "Duration (min)": [t.duration_minutes for t in pet_tasks],
                        "Priority": [t.priority for t in pet_tasks]
                    }
                    st.table(pet_data)
                else:
                    st.info(f"No tasks for {pet.name}")
    
    # Tab 4: Conflict Detection
    with tab4:
        if st.session_state.get('last_schedule'):
            conflicts = scheduler.check_conflicts()
            if conflicts:
                st.write("**⚠️ Scheduling Conflicts Detected:**")
                for conflict in conflicts:
                    st.warning(conflict)
            else:
                st.success("✅ **No scheduling conflicts!** Your schedule is optimized.")
else:
    st.info("Generate a schedule to see smart features")

st.divider()

# ============================================================================
# SCHEDULE DISPLAY
# ============================================================================

st.subheader("📅 Your Schedule")

if st.session_state['last_schedule'] is not None:
    schedule = st.session_state['last_schedule']
    
    if schedule.get_events():
        st.info(f"✅ Schedule: {len(schedule.get_events())} events")
        
        events_sorted = sorted(schedule.get_events(), key=lambda e: e.start_time)
        event_data = {
            "Time": [f"{event.start_time} - {event.end_time}" for event in events_sorted],
            "Task": [event.task_name for event in events_sorted],
            "Location": [event.location for event in events_sorted],
            "Duration": [f"{event.get_duration()} min" for event in events_sorted],
            "Priority": [f"⭐ {event.priority}" for event in events_sorted]
        }
        st.table(event_data)
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Duration", f"{schedule.get_total_duration()} min")
        with col2:
            st.metric("Wellbeing Score", f"{schedule.get_wellbeing_score():.2f}/1.0")
        with col3:
            st.metric("Events Scheduled", len(schedule.get_events()))
    else:
        st.info("Schedule generated but no events")
else:
    st.info("👆 Generate a schedule above to display it here")

st.divider()
st.caption("PawPal+ v1.0 | AI-Powered Pet Care Scheduling System")
