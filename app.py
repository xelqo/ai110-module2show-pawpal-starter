import streamlit as st
from pawpal_system import Owner, Pet, Task, Constraints, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ============================================================================
# INITIALIZE SESSION STATE (Persistent Vault)
# ============================================================================
# These objects persist across button clicks and reruns!

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

# Get references to persistent objects
owner = st.session_state['owner']

st.markdown(
    """
Welcome to **PawPal+** - Your Pet Care Planning Assistant!

Your data is saved in the session vault (st.session_state), so it persists as you navigate the app.
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

st.subheader("👤 Owner Information")
st.caption("Your information is stored in the session vault (persists across app navigation)")

owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
if owner_name != owner.name:
    owner.name = owner_name
    st.success(f"✅ Owner updated: {owner.name}")

st.divider()

st.subheader("🐾 Add Pets")
st.caption(f"You currently have {len(st.session_state['pets'])} pet(s)")

col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", placeholder="e.g., Mochi")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])

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

# Display current pets in vault
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
else:
    st.info("No pets yet. Add one above!")

st.divider()

st.subheader("📋 Add Tasks")
st.caption("Add tasks that need to be completed for your pets")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", placeholder="e.g., Morning walk", key="task_input")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration_input")
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
        st.success(f"✅ Task '{task_title}' added to vault!")
        st.rerun()
    else:
        st.error("Please enter a task title")

# Display current tasks in vault
if st.session_state['tasks']:
    st.write("**Tasks in Vault (will be assigned to pets):**")
    task_df = {
        "Task": [t.description for t in st.session_state['tasks']],
        "Duration (min)": [t.duration_minutes for t in st.session_state['tasks']],
        "Priority": [t.priority for t in st.session_state['tasks']],
        "Status": [("✓" if t.is_complete() else "○") for t in st.session_state['tasks']]
    }
    st.table(task_df)
    
    # Option to clear all tasks
    if st.button("🗑️ Clear All Tasks", key="clear_tasks_btn"):
        st.session_state['tasks'].clear()
        st.success("All tasks cleared!")
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("🕐 Build Schedule")
st.caption("Generate an optimized schedule for all your pets")

if st.button("🔄 Generate Schedule", key="generate_schedule_btn"):
    try:
        # Check if we have pets and tasks
        if not st.session_state['pets']:
            st.error("❌ Please add at least one pet before generating a schedule")
        elif not st.session_state['tasks']:
            st.error("❌ Please add at least one task before generating a schedule")
        else:
            # Create a fresh owner instance for scheduling (with tasks assigned)
            schedule_owner = Owner(
                name=owner.name,
                email=owner.email,
                phone_number=owner.phone_number,
                occupation=owner.occupation,
                owner_id=owner.owner_id
            )
            
            # Add all pets from vault to the schedule owner
            for pet in st.session_state['pets']:
                schedule_owner.add_pet(pet)
            
            # Assign tasks from vault to pets (cycle through if more tasks than pets)
            for i, task in enumerate(st.session_state['tasks']):
                pet_index = i % len(st.session_state['pets'])
                st.session_state['pets'][pet_index].add_task(task)
            
            # Create scheduler and generate schedule
            constraints = Constraints()
            constraints.set_city("San Francisco")
            constraints.set_climate("Temperate")
            constraints.set_available_exercise_hours([("08:00", "20:00")])
            constraints.set_weather_conditions(["Clear"])
            constraints.set_has_yard(True)
            
            scheduler = Scheduler(schedule_owner, constraints)
            schedule = scheduler.generate_optimal_schedule("2025-03-29")
            
            # Store in session state for persistence
            st.session_state['last_schedule'] = schedule
            st.success(f"✅ Schedule generated successfully! ({len(schedule.get_events())} events scheduled)")
    
    except Exception as e:
        st.error(f"Error generating schedule: {str(e)}")

# Display generated schedule from vault
st.subheader("� Schedule Display")

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
    st.info("👆 Generate a schedule above to see it displayed here. Your schedule will be stored in the vault!")
