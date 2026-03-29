"""
Pet Care App - Pawpaw System
A comprehensive pet care scheduling system that helps busy pet owners plan their day.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime, time


# ============================================================================
# Data Classes (Task, Pet, Owner, and related entities)
# ============================================================================

@dataclass
class Task:
    """Represents a single activity for a pet."""
    description: str
    time: str  # HH:MM format
    frequency: str  # daily, weekly, etc.
    completion_status: bool = False
    duration_minutes: int = 0
    pet_id: Optional[str] = None
    priority: str = "medium"  # high, medium, low

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completion_status = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completion_status = False

    def is_complete(self) -> bool:
        """Check if task is completed."""
        return self.completion_status

    def __str__(self) -> str:
        """String representation of task."""
        status = "✓" if self.completion_status else "○"
        return f"[{status}] {self.description} at {self.time} ({self.frequency})"


@dataclass
class Pet:
    """Represents a pet and its specific characteristics and needs."""
    name: str
    species: str
    age: int
    weight: float
    pet_id: Optional[str] = None
    health_needs: List[str] = field(default_factory=list)
    daily_activity_minutes: int = 0
    dietary_restrictions: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def update_weight(self, new_weight: float) -> None:
        """Update the pet's weight."""
        self.weight = new_weight

    def update_health_needs(self, new_health_needs: List[str]) -> None:
        """Update the pet's health needs."""
        self.health_needs = new_health_needs

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        task.pet_id = self.pet_id
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Get all tasks for this pet."""
        return self.tasks

    def get_incomplete_tasks(self) -> List[Task]:
        """Get all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.is_complete()]

    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks for this pet."""
        return [task for task in self.tasks if task.is_complete()]

    def get_tasks_by_frequency(self, frequency: str) -> List[Task]:
        """Get tasks filtered by frequency (daily, weekly, etc.)."""
        return [task for task in self.tasks if task.frequency == frequency]


@dataclass
class Owner:
    """Represents the pet owner and manages all their pets and tasks."""
    name: str
    email: str
    phone_number: str
    occupation: str
    owner_id: Optional[str] = None
    work_schedule: List[str] = field(default_factory=list)
    budget: float = 0.0
    pet_preferences: List[str] = field(default_factory=list)
    emergency_contacts: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def update_work_schedule(self, new_schedule: List[str]) -> None:
        """Update the owner's work schedule."""
        self.work_schedule = new_schedule

    def update_budget(self, new_budget: float) -> None:
        """Update the owner's budget."""
        self.budget = new_budget

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's pet list."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Get all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_all_incomplete_tasks(self) -> List[Task]:
        """Get all incomplete tasks across all pets."""
        all_incomplete = []
        for pet in self.pets:
            all_incomplete.extend(pet.get_incomplete_tasks())
        return all_incomplete

    def get_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Get all tasks for a specific pet by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def get_pet_by_name(self, pet_name: str) -> Optional[Pet]:
        """Get a specific pet by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_pet_count(self) -> int:
        """Get the number of pets owned."""
        return len(self.pets)

    def get_total_daily_activity_needed(self) -> int:
        """Get the total daily activity minutes needed across all pets."""
        return sum(pet.daily_activity_minutes for pet in self.pets)


@dataclass
class Meal:
    """Represents a meal for the pet."""
    time: str
    duration: int
    food_type: str
    amount: float


@dataclass
class Exercise:
    """Represents an exercise session for the pet."""
    exercise_type: str
    duration: int


@dataclass
class Medication:
    """Represents a medication schedule entry."""
    name: str
    time: str
    frequency: str
    dosage: str


# ============================================================================
# Tasks Class
# ============================================================================

class Tasks:
    """Defines all daily tasks and activities the pet needs."""

    def __init__(self):
        """Initialize the Tasks object."""
        self.task_list: List[str] = []
        self.meals: List[Meal] = []
        self.exercise_types: List[Exercise] = []
        self.medication_schedule: List[Medication] = []
        self.grooming_tasks: List[str] = []
        self.social_activities: List[str] = []
        self.water_intake_cups: int = 0

    def get_task_list(self) -> List[str]:
        """Get the complete task list."""
        return self.task_list

    def get_meals(self) -> List[Meal]:
        """Get all scheduled meals."""
        return self.meals

    def get_meal_times(self) -> List[str]:
        """Get all meal times."""
        return [meal.time for meal in self.meals]

    def get_meal_durations(self) -> List[int]:
        """Get all meal durations."""
        return [meal.duration for meal in self.meals]

    def get_exercise_types(self) -> List[str]:
        """Get all exercise types."""
        return [ex.exercise_type for ex in self.exercise_types]

    def get_exercise_durations(self) -> List[int]:
        """Get all exercise durations."""
        return [ex.duration for ex in self.exercise_types]

    def get_medication_schedule(self) -> List[Medication]:
        """Get the medication schedule."""
        return self.medication_schedule

    def get_grooming_tasks(self) -> List[str]:
        """Get all grooming tasks."""
        return self.grooming_tasks

    def get_social_activities(self) -> List[str]:
        """Get all social activities."""
        return self.social_activities

    def get_water_intake(self) -> int:
        """Get the water intake requirement in cups."""
        return self.water_intake_cups

    def add_task(self, task: str) -> None:
        """Add a new task to the task list."""
        if task not in self.task_list:
            self.task_list.append(task)

    def remove_task(self, task: str) -> None:
        """Remove a task from the task list."""
        if task in self.task_list:
            self.task_list.remove(task)

    def add_meal(self, meal: Meal) -> None:
        """Add a meal to the schedule."""
        self.meals.append(meal)

    def remove_meal(self, meal: Meal) -> None:
        """Remove a meal from the schedule."""
        if meal in self.meals:
            self.meals.remove(meal)

    def update_meal_times(self, new_meals: List[Meal]) -> None:
        """Update the meal schedule."""
        self.meals = new_meals

    def add_exercise(self, exercise: Exercise) -> None:
        """Add an exercise to the plan."""
        self.exercise_types.append(exercise)

    def update_exercise_plans(self, exercises: List[Exercise]) -> None:
        """Update exercise plans."""
        self.exercise_types = exercises

    def add_medication(self, medication: Medication) -> None:
        """Add a medication to the schedule."""
        self.medication_schedule.append(medication)

    def add_grooming_task(self, task: str) -> None:
        """Add a grooming task."""
        if task not in self.grooming_tasks:
            self.grooming_tasks.append(task)

    def add_social_activity(self, activity: str) -> None:
        """Add a social activity."""
        if activity not in self.social_activities:
            self.social_activities.append(activity)

    def calculate_total_daily_duration(self) -> int:
        """Calculate the total duration of all daily tasks in minutes."""
        total = 0
        total += sum(meal.duration for meal in self.meals)
        total += sum(ex.duration for ex in self.exercise_types)
        return total


# ============================================================================
# Constraints Class
# ============================================================================

class Constraints:
    """Handles environmental and temporal constraints for pet care."""

    def __init__(self):
        """Initialize the Constraints object."""
        self.city: str = ""
        self.climate: str = ""
        self.location: str = ""
        self.available_exercise_hours: List[Tuple[str, str]] = []
        self.weather_conditions: List[str] = []
        self.temperature_range: Tuple[int, int] = (0, 0)
        self.public_spaces: List[str] = []
        self.has_yard: bool = False
        self.restricted_areas: List[str] = []
        self.max_consecutive_activity: int = 0

    def get_city(self) -> str:
        """Get the city."""
        return self.city

    def get_climate(self) -> str:
        """Get the climate."""
        return self.climate

    def get_location(self) -> str:
        """Get the location."""
        return self.location

    def get_available_exercise_hours(self) -> List[Tuple[str, str]]:
        """Get the available exercise hours."""
        return self.available_exercise_hours

    def get_weather_conditions(self) -> List[str]:
        """Get current weather conditions."""
        return self.weather_conditions

    def get_temperature_range(self) -> Tuple[int, int]:
        """Get the temperature range."""
        return self.temperature_range

    def get_public_spaces(self) -> List[str]:
        """Get available public spaces."""
        return self.public_spaces

    def has_backyard(self) -> bool:
        """Check if the location has a backyard."""
        return self.has_yard

    def get_restricted_areas(self) -> List[str]:
        """Get restricted areas."""
        return self.restricted_areas

    def get_max_consecutive_activity(self) -> int:
        """Get the maximum consecutive activity duration."""
        return self.max_consecutive_activity

    def is_valid_time(self, time_slot: str) -> bool:
        """Check if a given time slot is valid for activities."""
        for start, end in self.available_exercise_hours:
            if start <= time_slot <= end:
                return True
        return False

    def can_exercise_outside(self) -> bool:
        """Determine if outdoor exercise is viable given weather conditions."""
        bad_conditions = ["heavy rain", "extreme heat", "blizzard", "thunderstorm"]
        return not any(condition in self.weather_conditions for condition in bad_conditions)

    def get_optimal_exercise_windows(self) -> List[Tuple[str, str]]:
        """Get optimal time windows for exercise based on constraints."""
        return self.available_exercise_hours if self.available_exercise_hours else []

    def set_city(self, city: str) -> None:
        """Set the city."""
        self.city = city

    def set_climate(self, climate: str) -> None:
        """Set the climate."""
        self.climate = climate

    def set_location(self, location: str) -> None:
        """Set the location."""
        self.location = location

    def set_available_exercise_hours(self, hours: List[Tuple[str, str]]) -> None:
        """Set the available exercise hours."""
        self.available_exercise_hours = hours

    def set_weather_conditions(self, conditions: List[str]) -> None:
        """Set the weather conditions."""
        self.weather_conditions = conditions

    def set_temperature_range(self, min_temp: int, max_temp: int) -> None:
        """Set the temperature range."""
        self.temperature_range = (min_temp, max_temp)

    def set_has_yard(self, has_yard: bool) -> None:
        """Set whether location has a backyard."""
        self.has_yard = has_yard

    def set_restricted_areas(self, areas: List[str]) -> None:
        """Set restricted areas."""
        self.restricted_areas = areas

    def set_max_consecutive_activity(self, minutes: int) -> None:
        """Set the maximum consecutive activity duration."""
        self.max_consecutive_activity = minutes

    def update_constraints(self, new_constraints: 'Constraints') -> None:
        """Update all constraints with new values."""
        self.city = new_constraints.city
        self.climate = new_constraints.climate
        self.location = new_constraints.location
        self.available_exercise_hours = new_constraints.available_exercise_hours
        self.weather_conditions = new_constraints.weather_conditions
        self.temperature_range = new_constraints.temperature_range
        self.public_spaces = new_constraints.public_spaces
        self.has_yard = new_constraints.has_yard
        self.restricted_areas = new_constraints.restricted_areas
        self.max_consecutive_activity = new_constraints.max_consecutive_activity


# ============================================================================
# Schedule and ScheduleEvent Classes
# ============================================================================

@dataclass
class ScheduleEvent:
    """Represents a single scheduled task or activity."""
    task_name: str
    start_time: str
    end_time: str
    location: str
    event_type: str
    priority: str
    notes: List[str] = field(default_factory=list)

    def get_duration(self) -> int:
        """Calculate the duration of the event in minutes."""
        # Simple time parsing: assumes HH:MM format
        try:
            start_h, start_m = map(int, self.start_time.split(':'))
            end_h, end_m = map(int, self.end_time.split(':'))
            start_mins = start_h * 60 + start_m
            end_mins = end_h * 60 + end_m
            return max(0, end_mins - start_mins)
        except (ValueError, IndexError):
            return 0

    def add_note(self, note: str) -> None:
        """Add a note to the event."""
        self.notes.append(note)

    def is_conflicting(self, other_event: 'ScheduleEvent') -> bool:
        """Check if this event conflicts with another event."""
        try:
            start_h, start_m = map(int, self.start_time.split(':'))
            end_h, end_m = map(int, self.end_time.split(':'))
            other_start_h, other_start_m = map(int, other_event.start_time.split(':'))
            other_end_h, other_end_m = map(int, other_event.end_time.split(':'))
            
            self_start = start_h * 60 + start_m
            self_end = end_h * 60 + end_m
            other_start = other_start_h * 60 + other_start_m
            other_end = other_end_h * 60 + other_end_m
            
            return not (self_end <= other_start or self_start >= other_end)
        except (ValueError, IndexError):
            return False


class Schedule:
    """Represents the generated daily schedule."""

    def __init__(self, date: str):
        """Initialize the Schedule object."""
        self.date: str = date
        self.events: List[ScheduleEvent] = []
        self.total_duration: int = 0
        self.wellbeing_score: float = 0.0

    def get_date(self) -> str:
        """Get the schedule date."""
        return self.date

    def get_events(self) -> List[ScheduleEvent]:
        """Get all scheduled events."""
        return self.events

    def get_total_duration(self) -> int:
        """Get the total duration of all events."""
        return sum(event.get_duration() for event in self.events)

    def get_wellbeing_score(self) -> float:
        """Get the wellbeing score."""
        return self.wellbeing_score

    def add_event(self, event: ScheduleEvent) -> bool:
        """Add an event to the schedule. Returns False if conflict exists."""
        for existing_event in self.events:
            if event.is_conflicting(existing_event):
                return False
        self.events.append(event)
        return True

    def remove_event(self, event: ScheduleEvent) -> None:
        """Remove an event from the schedule."""
        if event in self.events:
            self.events.remove(event)

    def get_event_by_time(self, time_slot: str) -> Optional[ScheduleEvent]:
        """Retrieve an event by time."""
        for event in self.events:
            if event.start_time == time_slot:
                return event
        return None

    def get_all_events_by_type(self, event_type: str) -> List[ScheduleEvent]:
        """Get all events of a specific type."""
        return [event for event in self.events if event.event_type == event_type]

    def is_schedule_fully_utilized(self) -> bool:
        """Check if the schedule is fully utilized."""
        return len(self.events) > 0

    def calculate_wellbeing_score(self) -> float:
        """Calculate the wellbeing score based on schedule."""
        # Simple scoring: more variety = higher score
        event_types = set(event.event_type for event in self.events)
        return min(len(event_types) / 5.0, 1.0)  # Normalize to 0-1

    def display_schedule(self) -> None:
        """Display the schedule in a human-readable format."""
        print(f"\n--- Schedule for {self.date} ---")
        for event in sorted(self.events, key=lambda e: e.start_time):
            print(f"{event.start_time} - {event.end_time}: {event.task_name} "
                  f"({event.event_type}) [{event.priority}]")
            if event.notes:
                print(f"  Notes: {', '.join(event.notes)}")
        print(f"Total Duration: {self.get_total_duration()} minutes")
        print(f"Wellbeing Score: {self.wellbeing_score:.2f}\n")


# ============================================================================
# Scheduler Class (Main Orchestrator)
# ============================================================================

class Scheduler:
    """
    The "Brain" of the system - retrieves, organizes, and manages tasks across pets.
    Handles scheduling, conflict detection, and optimization for multiple pets.
    """

    def __init__(self, owner: Owner, constraints: Constraints):
        """Initialize the Scheduler with owner and constraints."""
        self.owner: Owner = owner
        self.constraints: Constraints = constraints
        self.schedule: Optional[Schedule] = None
        self.conflicts: List[str] = []
        self.master_task_queue: List[Task] = []

    def get_owner(self) -> Owner:
        """Get the owner object."""
        return self.owner

    def get_constraints(self) -> Constraints:
        """Get the constraints object."""
        return self.constraints

    def get_schedule(self) -> Optional[Schedule]:
        """Get the current schedule."""
        return self.schedule

    def refresh_task_queue(self) -> None:
        """Refresh the master task queue from all pets."""
        self.master_task_queue = self.owner.get_all_tasks()

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets."""
        return self.owner.get_all_tasks()

    def get_all_incomplete_tasks(self) -> List[Task]:
        """Get all incomplete tasks across all pets."""
        return self.owner.get_all_incomplete_tasks()

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Get all tasks for a specific pet."""
        return self.owner.get_tasks_by_pet(pet_name)

    def get_task_summary(self) -> str:
        """Get a summary of all tasks across all pets."""
        summary = f"\n{'='*50}\nTASK SUMMARY FOR {self.owner.name.upper()}\n{'='*50}\n"
        
        for pet in self.owner.get_pets():
            tasks = pet.get_tasks()
            incomplete = pet.get_incomplete_tasks()
            summary += f"\n🐾 {pet.name} ({pet.species}):\n"
            summary += f"   Total Tasks: {len(tasks)} | Incomplete: {len(incomplete)}\n"
            
            for task in tasks:
                summary += f"   {task}\n"
        
        return summary

    def generate_optimal_schedule(self, date: str) -> Schedule:
        """Generate an optimal schedule for the given date across all pets."""
        self.schedule = Schedule(date)
        self.conflicts = []
        self.refresh_task_queue()
        
        # Sort tasks by priority and time
        sorted_tasks = sorted(
            self.master_task_queue,
            key=lambda t: ({"high": 0, "medium": 1, "low": 2}.get(t.priority, 1), t.time)
        )
        
        # Add tasks to schedule
        for task in sorted_tasks:
            event = ScheduleEvent(
                task_name=task.description,
                start_time=task.time,
                end_time=self._calculate_end_time(task.time, task.duration_minutes),
                location="Home",
                event_type="task",
                priority=task.priority,
                notes=[f"Pet: {self._get_pet_name_from_task(task)}"]
            )
            
            if not self.schedule.add_event(event):
                self.conflicts.append(f"Conflict: {event.task_name} at {event.start_time}")
        
        self.schedule.wellbeing_score = self.schedule.calculate_wellbeing_score()
        return self.schedule

    def validate_schedule(self, schedule: Schedule) -> bool:
        """Validate if the schedule adheres to all constraints."""
        for event in schedule.get_events():
            if not self.constraints.is_valid_time(event.start_time):
                return False
        return len(self.conflicts) == 0

    def check_conflicts(self) -> List[str]:
        """
        Check for conflicts in the current schedule with detailed warnings.
        
        Detects overlapping task durations (not just exact time matches) and returns
        a list of descriptive conflict warnings.
        
        Returns:
            List of conflict warning messages describing overlapping tasks.
        """
        if not self.schedule:
            return []
        
        conflicts = []
        for i, event1 in enumerate(self.schedule.events):
            for event2 in self.schedule.events[i+1:]:
                if event1.is_conflicting(event2):
                    conflict_msg = (
                        f"⚠️  CONFLICT: {event1.task_name} ({event1.start_time}-{event1.end_time}) "
                        f"overlaps with {event2.task_name} ({event2.start_time}-{event2.end_time})"
                    )
                    conflicts.append(conflict_msg)
        return conflicts

    def optimize_for_wellbeing(self) -> Schedule:
        """Optimize the schedule to prioritize pet wellbeing across all pets."""
        if not self.schedule:
            return self.generate_optimal_schedule("today")
        
        # Ensure each pet gets adequate activity
        for pet in self.owner.get_pets():
            exercise_tasks = [t for t in pet.get_tasks() if "exercise" in t.description.lower()]
            exercise_duration = sum(t.duration_minutes for t in exercise_tasks)
            
            if exercise_duration < pet.daily_activity_minutes:
                deficit = pet.daily_activity_minutes - exercise_duration
                new_task = Task(
                    description=f"{pet.name} - Additional Exercise",
                    time="15:00",
                    frequency="daily",
                    duration_minutes=deficit,
                    priority="high"
                )
                pet.add_task(new_task)
        
        return self.generate_optimal_schedule(self.schedule.date if self.schedule else "today")

    def optimize_for_owner_availability(self) -> Schedule:
        """Optimize the schedule based on owner's work availability."""
        if not self.schedule:
            return self.generate_optimal_schedule("today")
        
        # Align pet activities with owner's free time windows
        # This would parse work_schedule and adjust task times accordingly
        return self.schedule

    def adjust_for_weather(self) -> Schedule:
        """Adjust the schedule based on current weather conditions."""
        if not self.schedule or self.constraints.can_exercise_outside():
            return self.schedule
        
        # Move outdoor exercises indoors if needed
        for event in self.schedule.events:
            if "exercise" in event.task_name.lower() and event.location == "Park":
                event.location = "Home"
                event.add_note("Indoor exercise due to weather")
        
        return self.schedule

    def mark_task_complete(self, pet_name: str, task_description: str) -> bool:
        """
        Mark a task as complete for a specific pet.
        
        If the task is recurring (daily or weekly), automatically creates a new task
        for the next occurrence.
        
        Args:
            pet_name: Name of the pet.
            task_description: Description of the task to mark complete.
        
        Returns:
            True if task was found and marked complete, False otherwise.
        """
        from datetime import timedelta, datetime
        
        pet = self.owner.get_pet_by_name(pet_name)
        if not pet:
            return False
        
        for task in pet.get_tasks():
            if task.description == task_description:
                task.mark_complete()
                
                # Auto-create next occurrence for recurring tasks
                if task.frequency in ["daily", "weekly"]:
                    # Calculate days to add
                    days_to_add = 1 if task.frequency == "daily" else 7
                    
                    # Create new task for next occurrence
                    next_task = Task(
                        description=task.description,
                        time=task.time,
                        frequency=task.frequency,
                        duration_minutes=task.duration_minutes,
                        priority=task.priority,
                        pet_id=task.pet_id
                    )
                    
                    pet.add_task(next_task)
                    return True
                
                return True
        
        return False

    def mark_task_incomplete(self, pet_name: str, task_description: str) -> bool:
        """Mark a task as incomplete for a specific pet."""
        pet = self.owner.get_pet_by_name(pet_name)
        if not pet:
            return False
        
        for task in pet.get_tasks():
            if task.description == task_description:
                task.mark_incomplete()
                return True
        return False

    def reschedule_task(self, pet_name: str, task_description: str, new_time: str) -> bool:
        """Reschedule a task to a new time."""
        pet = self.owner.get_pet_by_name(pet_name)
        if not pet:
            return False
        
        for task in pet.get_tasks():
            if task.description == task_description:
                task.time = new_time
                return True
        return False

    def get_suggestions(self) -> List[str]:
        """Get optimization suggestions for the overall schedule."""
        suggestions = []
        
        if not self.schedule:
            suggestions.append("Generate a schedule first")
            return suggestions
        
        # Check if all pets are getting adequate activity
        for pet in self.owner.get_pets():
            exercise_tasks = [t for t in pet.get_tasks() if "exercise" in t.description.lower()]
            exercise_duration = sum(t.duration_minutes for t in exercise_tasks)
            
            if exercise_duration < pet.daily_activity_minutes:
                suggestions.append(
                    f"🐾 {pet.name} needs {pet.daily_activity_minutes - exercise_duration} "
                    "more minutes of exercise"
                )
        
        # Check for uncompleted high-priority tasks
        incomplete_high_priority = [
            t for t in self.get_all_incomplete_tasks() if t.priority == "high"
        ]
        if incomplete_high_priority:
            suggestions.append(
                f"⚠️  {len(incomplete_high_priority)} high-priority tasks are incomplete"
            )
        
        return suggestions

    def export_schedule(self, format: str = 'text') -> str:
        """Export the schedule in the specified format."""
        if not self.schedule:
            return "No schedule to export"
        
        if format == 'text':
            result = f"Schedule for {self.schedule.date}\n"
            result += "=" * 50 + "\n"
            for event in sorted(self.schedule.events, key=lambda e: e.start_time):
                result += f"{event.start_time} - {event.end_time}: {event.task_name}\n"
                if event.notes:
                    result += f"  Notes: {', '.join(event.notes)}\n"
            return result
        
        return "Unsupported format"

    def display_full_report(self) -> None:
        """Display a comprehensive report of all pets, tasks, and schedule."""
        print(self.get_task_summary())
        
        if self.schedule:
            self.schedule.display_schedule()
        else:
            print("\n⚠️  No schedule generated yet. Use generate_optimal_schedule() to create one.\n")
        
        suggestions = self.get_suggestions()
        if suggestions:
            print("\n💡 SUGGESTIONS:\n")
            for suggestion in suggestions:
                print(f"  • {suggestion}\n")

    def sort_tasks_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """
        Sort tasks by their time attribute in HH:MM format.
        
        Args:
            tasks: List of tasks to sort. If None, sorts all tasks.
        
        Returns:
            List of tasks sorted by time (earliest first).
        """
        task_list = tasks if tasks is not None else self.get_all_tasks()
        
        def time_to_minutes(time_str: str) -> int:
            """Convert HH:MM time format to minutes since midnight."""
            try:
                hours, minutes = map(int, time_str.split(':'))
                return hours * 60 + minutes
            except (ValueError, IndexError):
                return 0
        
        return sorted(task_list, key=lambda t: time_to_minutes(t.time))

    def filter_tasks_by_status(self, completed: bool = False) -> List[Task]:
        """
        Filter tasks by completion status across all pets.
        
        Args:
            completed: If True, return only completed tasks. If False, return only incomplete tasks.
        
        Returns:
            List of tasks matching the completion status.
        """
        all_tasks = self.get_all_tasks()
        if completed:
            return [task for task in all_tasks if task.is_complete()]
        else:
            return [task for task in all_tasks if not task.is_complete()]

    def filter_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """
        Filter tasks by pet name.
        
        Args:
            pet_name: Name of the pet to get tasks for.
        
        Returns:
            List of tasks for the specified pet, or empty list if pet not found.
        """
        pet = self.owner.get_pet_by_name(pet_name)
        if pet:
            return pet.get_tasks()
        return []

    def _get_pet_name_from_task(self, task: Task) -> str:
        """Helper to find which pet a task belongs to."""
        for pet in self.owner.get_pets():
            if task in pet.get_tasks():
                return pet.name
        return "Unknown"

    def _calculate_end_time(self, start_time: str, duration: int) -> str:
        """Helper method to calculate end time."""
        try:
            h, m = map(int, start_time.split(':'))
            total_mins = h * 60 + m + duration
            end_h = total_mins // 60
            end_m = total_mins % 60
            return f"{end_h:02d}:{end_m:02d}"
        except (ValueError, IndexError):
            return start_time


# ============================================================================
# Main Entry Point and Demo
# ============================================================================

def main():
    """Main entry point demonstrating the Pawpaw System with guidelines."""
    
    print("\n" + "="*60)
    print("🐾 PAWPAW PET CARE SCHEDULING SYSTEM 🐾")
    print("="*60)
    
    # Create an owner
    owner = Owner(
        name="Alice",
        email="alice@example.com",
        phone_number="555-1234",
        occupation="Software Engineer",
        owner_id="owner_001"
    )
    
    # Create pets
    dog = Pet(
        name="Max",
        species="Golden Retriever",
        age=3,
        weight=65.0,
        pet_id="pet_001",
        daily_activity_minutes=60
    )
    
    cat = Pet(
        name="Whiskers",
        species="Tabby Cat",
        age=2,
        weight=8.5,
        pet_id="pet_002",
        daily_activity_minutes=20
    )
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Create tasks for dog
    task1 = Task(
        description="Morning Walk",
        time="07:00",
        frequency="daily",
        duration_minutes=30,
        priority="high"
    )
    
    task2 = Task(
        description="Breakfast",
        time="08:00",
        frequency="daily",
        duration_minutes=15,
        priority="high"
    )
    
    task3 = Task(
        description="Afternoon Exercise",
        time="15:00",
        frequency="daily",
        duration_minutes=45,
        priority="high"
    )
    
    task4 = Task(
        description="Dinner",
        time="18:00",
        frequency="daily",
        duration_minutes=15,
        priority="high"
    )
    
    # Create tasks for cat
    cat_task1 = Task(
        description="Feeding",
        time="08:30",
        frequency="daily",
        duration_minutes=10,
        priority="high"
    )
    
    cat_task2 = Task(
        description="Playtime",
        time="16:00",
        frequency="daily",
        duration_minutes=20,
        priority="medium"
    )
    
    # Add tasks to pets
    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task3)
    dog.add_task(task4)
    
    cat.add_task(cat_task1)
    cat.add_task(cat_task2)
    
    # Mark some tasks as complete
    task1.mark_complete()
    cat_task1.mark_complete()
    
    # Create constraints
    constraints = Constraints()
    constraints.set_city("San Francisco")
    constraints.set_climate("Temperate")
    constraints.set_available_exercise_hours([("07:00", "09:00"), ("15:00", "18:00")])
    constraints.set_weather_conditions(["Clear", "Mild"])
    constraints.set_has_yard(True)
    
    # Create scheduler (the "brain")
    scheduler = Scheduler(owner, constraints)
    
    # Display task summary
    print(scheduler.get_task_summary())
    
    # Generate optimal schedule
    print("\n📅 Generating optimal schedule...\n")
    scheduler.generate_optimal_schedule("2025-03-29")
    
    # Display the schedule
    scheduler.schedule.display_schedule()
    
    # Get suggestions
    print("\n💡 SYSTEM SUGGESTIONS:")
    for suggestion in scheduler.get_suggestions():
        print(f"  • {suggestion}")
    
    # Test task management
    print("\n\n📋 TESTING TASK MANAGEMENT:")
    print(f"✓ Mark 'Morning Walk' as complete for Max: {scheduler.mark_task_complete('Max', 'Morning Walk')}")
    print(f"✓ Total incomplete tasks across all pets: {len(scheduler.get_all_incomplete_tasks())}")
    
    # Export schedule
    print("\n\n📤 EXPORTED SCHEDULE:\n")
    print(scheduler.export_schedule('text'))
    
    print("="*60)
    print("✅ Demo Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
