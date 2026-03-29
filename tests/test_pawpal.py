"""
Unit Tests for PawPal System
Tests core functionality of the pawpal_system module including task management,
pet management, and scheduling.
"""

import pytest
from pawpal_system import Task, Pet, Owner, Constraints, Scheduler, ScheduleEvent, Schedule


# ============================================================================
# Task Tests
# ============================================================================

class TestTask:
    """Test suite for Task class functionality."""
    
    def test_task_creation(self):
        """Test that a task can be created with proper attributes."""
        task = Task(
            description="Morning Walk",
            time="07:00",
            frequency="daily",
            duration_minutes=30,
            priority="high"
        )
        
        assert task.description == "Morning Walk"
        assert task.time == "07:00"
        assert task.frequency == "daily"
        assert task.duration_minutes == 30
        assert task.priority == "high"
    
    def test_task_completion_status_changes(self):
        """Verify that calling mark_complete() changes the task's completion status."""
        task = Task(
            description="Feed Dog",
            time="08:00",
            frequency="daily",
            duration_minutes=15,
            priority="high"
        )
        
        # Initially, task should be incomplete
        assert task.is_complete() is False
        assert task.completion_status is False
        
        # Mark task as complete
        task.mark_complete()
        
        # Now task should be complete
        assert task.is_complete() is True
        assert task.completion_status is True
        
        # Mark task as incomplete
        task.mark_incomplete()
        
        # Now task should be incomplete again
        assert task.is_complete() is False
        assert task.completion_status is False
    
    def test_task_string_representation(self):
        """Test that task displays correctly as a string."""
        task = Task(
            description="Playtime",
            time="14:00",
            frequency="daily",
            duration_minutes=20,
            priority="medium"
        )
        
        task_str = str(task)
        assert "Playtime" in task_str
        assert "14:00" in task_str
        assert "daily" in task_str


# ============================================================================
# Pet Tests
# ============================================================================

class TestPet:
    """Test suite for Pet class functionality."""
    
    def test_pet_creation(self):
        """Test that a pet can be created with proper attributes."""
        pet = Pet(
            name="Max",
            species="Golden Retriever",
            age=3,
            weight=65.0,
            pet_id="pet_001",
            daily_activity_minutes=60
        )
        
        assert pet.name == "Max"
        assert pet.species == "Golden Retriever"
        assert pet.age == 3
        assert pet.weight == 65.0
        assert pet.daily_activity_minutes == 60
    
    def test_task_addition_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(
            name="Buddy",
            species="Labrador",
            age=4,
            weight=70.0,
            pet_id="pet_002"
        )
        
        # Initially, pet should have no tasks
        assert len(pet.get_tasks()) == 0
        
        # Create and add first task
        task1 = Task(
            description="Morning Walk",
            time="07:00",
            frequency="daily",
            duration_minutes=30,
            priority="high"
        )
        pet.add_task(task1)
        
        # Task count should be 1
        assert len(pet.get_tasks()) == 1
        assert task1 in pet.get_tasks()
        
        # Add a second task
        task2 = Task(
            description="Afternoon Exercise",
            time="14:00",
            frequency="daily",
            duration_minutes=45,
            priority="high"
        )
        pet.add_task(task2)
        
        # Task count should now be 2
        assert len(pet.get_tasks()) == 2
        assert task2 in pet.get_tasks()
    
    def test_pet_incomplete_tasks(self):
        """Test that incomplete tasks are correctly identified."""
        pet = Pet(
            name="Whiskers",
            species="Cat",
            age=2,
            weight=10.0,
            pet_id="pet_003"
        )
        
        # Add three tasks
        task1 = Task(description="Feeding", time="08:00", frequency="daily", priority="high")
        task2 = Task(description="Play", time="12:00", frequency="daily", priority="medium")
        task3 = Task(description="Grooming", time="16:00", frequency="daily", priority="medium")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # All tasks should be incomplete
        assert len(pet.get_incomplete_tasks()) == 3
        assert len(pet.get_completed_tasks()) == 0
        
        # Mark one task as complete
        task1.mark_complete()
        
        # Now we should have 2 incomplete and 1 completed
        assert len(pet.get_incomplete_tasks()) == 2
        assert len(pet.get_completed_tasks()) == 1
    
    def test_pet_remove_task(self):
        """Test that removing a task decreases the task count."""
        pet = Pet(
            name="Max",
            species="Dog",
            age=3,
            weight=50.0,
            pet_id="pet_004"
        )
        
        task = Task(description="Walk", time="07:00", frequency="daily", priority="high")
        pet.add_task(task)
        
        assert len(pet.get_tasks()) == 1
        
        pet.remove_task(task)
        
        assert len(pet.get_tasks()) == 0


# ============================================================================
# Owner Tests
# ============================================================================

class TestOwner:
    """Test suite for Owner class functionality."""
    
    def test_owner_creation(self):
        """Test that an owner can be created with proper attributes."""
        owner = Owner(
            name="Alice",
            email="alice@example.com",
            phone_number="555-1234",
            occupation="Software Engineer",
            owner_id="owner_001"
        )
        
        assert owner.name == "Alice"
        assert owner.email == "alice@example.com"
        assert owner.phone_number == "555-1234"
        assert owner.occupation == "Software Engineer"
    
    def test_owner_add_pet(self):
        """Test that adding pets to an owner increases pet count."""
        owner = Owner(
            name="Bob",
            email="bob@example.com",
            phone_number="555-5678",
            occupation="Teacher",
            owner_id="owner_002"
        )
        
        # Initially, owner should have no pets
        assert owner.get_pet_count() == 0
        
        # Create and add first pet
        pet1 = Pet(
            name="Max",
            species="Dog",
            age=3,
            weight=60.0,
            pet_id="pet_001"
        )
        owner.add_pet(pet1)
        
        assert owner.get_pet_count() == 1
        assert pet1 in owner.get_pets()
        
        # Add second pet
        pet2 = Pet(
            name="Whiskers",
            species="Cat",
            age=2,
            weight=10.0,
            pet_id="pet_002"
        )
        owner.add_pet(pet2)
        
        assert owner.get_pet_count() == 2
    
    def test_owner_get_pet_by_name(self):
        """Test that retrieving a pet by name works correctly."""
        owner = Owner(
            name="Sarah",
            email="sarah@example.com",
            phone_number="555-9999",
            occupation="Vet",
            owner_id="owner_003"
        )
        
        pet = Pet(
            name="Buddy",
            species="Dog",
            age=4,
            weight=70.0,
            pet_id="pet_001"
        )
        owner.add_pet(pet)
        
        retrieved_pet = owner.get_pet_by_name("Buddy")
        assert retrieved_pet is not None
        assert retrieved_pet.name == "Buddy"
        
        # Try to retrieve non-existent pet
        non_existent = owner.get_pet_by_name("NonExistent")
        assert non_existent is None


# ============================================================================
# Schedule Tests
# ============================================================================

class TestScheduleEvent:
    """Test suite for ScheduleEvent class functionality."""
    
    def test_schedule_event_creation(self):
        """Test that a schedule event can be created with proper attributes."""
        event = ScheduleEvent(
            task_name="Morning Walk",
            start_time="07:00",
            end_time="07:30",
            location="Park",
            event_type="exercise",
            priority="high"
        )
        
        assert event.task_name == "Morning Walk"
        assert event.start_time == "07:00"
        assert event.end_time == "07:30"
        assert event.location == "Park"
        assert event.event_type == "exercise"
        assert event.priority == "high"
    
    def test_schedule_event_duration_calculation(self):
        """Test that event duration is calculated correctly."""
        event = ScheduleEvent(
            task_name="Exercise",
            start_time="14:00",
            end_time="14:45",
            location="Park",
            event_type="exercise",
            priority="high"
        )
        
        # Duration should be 45 minutes
        assert event.get_duration() == 45
    
    def test_schedule_event_conflict_detection(self):
        """Test that event conflicts are detected correctly."""
        event1 = ScheduleEvent(
            task_name="Walk",
            start_time="07:00",
            end_time="07:30",
            location="Park",
            event_type="exercise",
            priority="high"
        )
        
        event2 = ScheduleEvent(
            task_name="Feeding",
            start_time="07:15",
            end_time="07:25",
            location="Home",
            event_type="feeding",
            priority="high"
        )
        
        # Events should conflict
        assert event1.is_conflicting(event2) is True
        assert event2.is_conflicting(event1) is True
    
    def test_schedule_event_no_conflict(self):
        """Test that non-conflicting events are detected correctly."""
        event1 = ScheduleEvent(
            task_name="Walk",
            start_time="07:00",
            end_time="07:30",
            location="Park",
            event_type="exercise",
            priority="high"
        )
        
        event2 = ScheduleEvent(
            task_name="Feeding",
            start_time="08:00",
            end_time="08:15",
            location="Home",
            event_type="feeding",
            priority="high"
        )
        
        # Events should NOT conflict
        assert event1.is_conflicting(event2) is False
        assert event2.is_conflicting(event1) is False


class TestSchedule:
    """Test suite for Schedule class functionality."""
    
    def test_schedule_creation(self):
        """Test that a schedule can be created with a date."""
        schedule = Schedule("2025-03-29")
        
        assert schedule.get_date() == "2025-03-29"
        assert len(schedule.get_events()) == 0
    
    def test_schedule_add_event(self):
        """Test that events can be added to a schedule."""
        schedule = Schedule("2025-03-29")
        
        event = ScheduleEvent(
            task_name="Walk",
            start_time="07:00",
            end_time="07:30",
            location="Park",
            event_type="exercise",
            priority="high"
        )
        
        result = schedule.add_event(event)
        
        assert result is True
        assert len(schedule.get_events()) == 1
        assert event in schedule.get_events()
    
    def test_schedule_prevents_conflicting_events(self):
        """Test that conflicting events cannot be added."""
        schedule = Schedule("2025-03-29")
        
        event1 = ScheduleEvent(
            task_name="Walk",
            start_time="07:00",
            end_time="07:30",
            location="Park",
            event_type="exercise",
            priority="high"
        )
        
        event2 = ScheduleEvent(
            task_name="Feeding",
            start_time="07:15",
            end_time="07:25",
            location="Home",
            event_type="feeding",
            priority="high"
        )
        
        # Add first event
        result1 = schedule.add_event(event1)
        assert result1 is True
        
        # Try to add conflicting event
        result2 = schedule.add_event(event2)
        assert result2 is False
        assert len(schedule.get_events()) == 1


# ============================================================================
# Scheduler Tests
# ============================================================================

class TestScheduler:
    """Test suite for Scheduler class functionality."""
    
    def test_scheduler_creation(self):
        """Test that a scheduler can be created with owner and constraints."""
        owner = Owner(
            name="Alice",
            email="alice@example.com",
            phone_number="555-1234",
            occupation="Engineer",
            owner_id="owner_001"
        )
        
        constraints = Constraints()
        scheduler = Scheduler(owner, constraints)
        
        assert scheduler.get_owner() == owner
        assert scheduler.get_constraints() == constraints
    
    def test_scheduler_generate_schedule(self):
        """Test that a scheduler can generate a schedule."""
        owner = Owner(
            name="Bob",
            email="bob@example.com",
            phone_number="555-5678",
            occupation="Vet",
            owner_id="owner_002"
        )
        
        pet = Pet(
            name="Max",
            species="Dog",
            age=3,
            weight=60.0,
            pet_id="pet_001"
        )
        
        task = Task(
            description="Morning Walk",
            time="07:00",
            frequency="daily",
            duration_minutes=30,
            priority="high"
        )
        
        pet.add_task(task)
        owner.add_pet(pet)
        
        constraints = Constraints()
        scheduler = Scheduler(owner, constraints)
        
        schedule = scheduler.generate_optimal_schedule("2025-03-29")
        
        assert schedule is not None
        assert schedule.get_date() == "2025-03-29"
        assert len(schedule.get_events()) > 0
    
    def test_scheduler_get_all_tasks(self):
        """Test that scheduler can retrieve all tasks across all pets."""
        owner = Owner(
            name="Sarah",
            email="sarah@example.com",
            phone_number="555-9999",
            occupation="Engineer",
            owner_id="owner_003"
        )
        
        pet1 = Pet(name="Max", species="Dog", age=3, weight=60.0, pet_id="pet_001")
        pet2 = Pet(name="Whiskers", species="Cat", age=2, weight=10.0, pet_id="pet_002")
        
        task1 = Task(description="Walk", time="07:00", frequency="daily", priority="high")
        task2 = Task(description="Feed", time="08:00", frequency="daily", priority="high")
        task3 = Task(description="Play", time="14:00", frequency="daily", priority="medium")
        
        pet1.add_task(task1)
        pet1.add_task(task2)
        pet2.add_task(task3)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        constraints = Constraints()
        scheduler = Scheduler(owner, constraints)
        
        all_tasks = scheduler.get_all_tasks()
        
        assert len(all_tasks) == 3
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for the complete PawPal system."""
    
    def test_complete_workflow(self):
        """Test a complete workflow: create owner, add pets, add tasks, generate schedule."""
        # Create owner
        owner = Owner(
            name="John",
            email="john@example.com",
            phone_number="555-1111",
            occupation="Freelancer",
            owner_id="owner_001"
        )
        
        # Create pets
        dog = Pet(
            name="Buddy",
            species="Labrador",
            age=4,
            weight=70.0,
            pet_id="pet_001",
            daily_activity_minutes=90
        )
        
        cat = Pet(
            name="Mittens",
            species="Cat",
            age=2,
            weight=9.0,
            pet_id="pet_002",
            daily_activity_minutes=30
        )
        
        # Add pets to owner
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        assert owner.get_pet_count() == 2
        
        # Create and add tasks for dog
        task1 = Task(
            description="Morning Walk",
            time="07:00",
            frequency="daily",
            duration_minutes=30,
            priority="high"
        )
        task2 = Task(
            description="Exercise",
            time="14:00",
            frequency="daily",
            duration_minutes=45,
            priority="high"
        )
        dog.add_task(task1)
        dog.add_task(task2)
        
        # Create and add tasks for cat
        task3 = Task(
            description="Feeding",
            time="08:00",
            frequency="daily",
            duration_minutes=10,
            priority="high"
        )
        task4 = Task(
            description="Play",
            time="16:00",
            frequency="daily",
            duration_minutes=20,
            priority="medium"
        )
        cat.add_task(task3)
        cat.add_task(task4)
        
        # Verify task counts
        assert len(dog.get_tasks()) == 2
        assert len(cat.get_tasks()) == 2
        
        # Create constraints and scheduler
        constraints = Constraints()
        scheduler = Scheduler(owner, constraints)
        
        # Generate schedule
        schedule = scheduler.generate_optimal_schedule("2025-03-29")
        
        # Verify schedule
        assert schedule is not None
        assert len(schedule.get_events()) == 4
        
        # Mark some tasks as complete
        task1.mark_complete()
        task3.mark_complete()
        
        # Verify completion
        assert task1.is_complete() is True
        assert task3.is_complete() is True
        assert len(scheduler.get_all_incomplete_tasks()) == 2
