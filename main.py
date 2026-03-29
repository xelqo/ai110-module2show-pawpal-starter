"""
Testing Ground for PawPal System
This script demonstrates the core functionality of the pawpal_system module
by creating owners, pets, tasks, and generating a daily schedule.
"""

from pawpal_system import Owner, Pet, Task, Constraints, Scheduler


def main():
    """Main testing script for the PawPal system."""
    
    print("\n" + "="*70)
    print("🐾 PAWPAL SYSTEM - DAILY SCHEDULE TESTING 🐾")
    print("="*70)
    
    # ========================================================================
    # STEP 1: Create an Owner
    # ========================================================================
    print("\n📝 STEP 1: Creating Owner...")
    owner = Owner(
        name="Sarah Johnson",
        email="sarah.johnson@email.com",
        phone_number="555-0123",
        occupation="Veterinary Technician",
        owner_id="owner_001",
        work_schedule=["9:00-17:00 Mon-Fri"],
        budget=2000.0
    )
    print(f"✓ Created owner: {owner.name}")
    print(f"  • Occupation: {owner.occupation}")
    print(f"  • Email: {owner.email}")
    
    # ========================================================================
    # STEP 2: Create Multiple Pets
    # ========================================================================
    print("\n🐶 STEP 2: Creating Pets...")
    
    # Pet 1: Dog
    dog = Pet(
        name="Buddy",
        species="Labrador Retriever",
        age=4,
        weight=65.0,
        pet_id="pet_001",
        daily_activity_minutes=90,
        allergies=["wheat"],
        health_needs=["Joint support"]
    )
    print(f"✓ Created pet: {dog.name} ({dog.species})")
    print(f"  • Age: {dog.age} years | Weight: {dog.weight} lbs")
    print(f"  • Daily activity needed: {dog.daily_activity_minutes} minutes")
    
    # Pet 2: Cat
    cat = Pet(
        name="Whiskers",
        species="Maine Coon",
        age=2,
        weight=12.0,
        pet_id="pet_002",
        daily_activity_minutes=30,
        health_needs=["Regular dental checkups"]
    )
    print(f"✓ Created pet: {cat.name} ({cat.species})")
    print(f"  • Age: {cat.age} years | Weight: {cat.weight} lbs")
    print(f"  • Daily activity needed: {cat.daily_activity_minutes} minutes")
    
    # Pet 3: Rabbit
    rabbit = Pet(
        name="Hopscotch",
        species="Holland Lop Rabbit",
        age=1,
        weight=4.5,
        pet_id="pet_003",
        daily_activity_minutes=60,
        dietary_restrictions=["No iceberg lettuce", "No chocolate"]
    )
    print(f"✓ Created pet: {rabbit.name} ({rabbit.species})")
    print(f"  • Age: {rabbit.age} years | Weight: {rabbit.weight} lbs")
    print(f"  • Daily activity needed: {rabbit.daily_activity_minutes} minutes")
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    owner.add_pet(rabbit)
    
    print(f"\n✓ Total pets owned by {owner.name}: {owner.get_pet_count()}")
    print(f"✓ Total daily activity minutes needed: {owner.get_total_daily_activity_needed()}")
    
    # ========================================================================
    # STEP 3: Add Tasks with Different Times
    # ========================================================================
    print("\n📋 STEP 3: Adding Tasks to Pets...")
    
    # Tasks for Buddy (Dog)
    task_dog1 = Task(
        description="Morning Walk",
        time="07:00",
        frequency="daily",
        duration_minutes=30,
        priority="high"
    )
    
    task_dog2 = Task(
        description="Breakfast & Medication",
        time="08:00",
        frequency="daily",
        duration_minutes=20,
        priority="high"
    )
    
    task_dog3 = Task(
        description="Afternoon Exercise at Park",
        time="14:00",
        frequency="daily",
        duration_minutes=45,
        priority="high"
    )
    
    task_dog4 = Task(
        description="Dinner",
        time="18:30",
        frequency="daily",
        duration_minutes=15,
        priority="high"
    )
    
    dog.add_task(task_dog1)
    dog.add_task(task_dog2)
    dog.add_task(task_dog3)
    dog.add_task(task_dog4)
    
    print(f"\n✓ Added {len(dog.get_tasks())} tasks for {dog.name}:")
    for task in dog.get_tasks():
        print(f"  • {task}")
    
    # Tasks for Whiskers (Cat)
    task_cat1 = Task(
        description="Feeding",
        time="07:30",
        frequency="daily",
        duration_minutes=10,
        priority="high"
    )
    
    task_cat2 = Task(
        description="Interactive Play",
        time="12:00",
        frequency="daily",
        duration_minutes=20,
        priority="medium"
    )
    
    task_cat3 = Task(
        description="Evening Playtime",
        time="19:00",
        frequency="daily",
        duration_minutes=25,
        priority="medium"
    )
    
    cat.add_task(task_cat1)
    cat.add_task(task_cat2)
    cat.add_task(task_cat3)
    
    print(f"\n✓ Added {len(cat.get_tasks())} tasks for {cat.name}:")
    for task in cat.get_tasks():
        print(f"  • {task}")
    
    # Tasks for Hopscotch (Rabbit)
    task_rabbit1 = Task(
        description="Fresh Hay & Vegetables",
        time="07:00",
        frequency="daily",
        duration_minutes=15,
        priority="high"
    )
    
    task_rabbit2 = Task(
        description="Free Roam Exercise",
        time="11:00",
        frequency="daily",
        duration_minutes=45,
        priority="high"
    )
    
    task_rabbit3 = Task(
        description="Evening Feeding",
        time="17:30",
        frequency="daily",
        duration_minutes=15,
        priority="high"
    )
    
    rabbit.add_task(task_rabbit1)
    rabbit.add_task(task_rabbit2)
    rabbit.add_task(task_rabbit3)
    
    print(f"\n✓ Added {len(rabbit.get_tasks())} tasks for {rabbit.name}:")
    for task in rabbit.get_tasks():
        print(f"  • {task}")
    
    # ========================================================================
    # STEP 4: Set Up Constraints
    # ========================================================================
    print("\n🌍 STEP 4: Setting Up Environmental Constraints...")
    
    constraints = Constraints()
    constraints.set_city("Portland, Oregon")
    constraints.set_climate("Temperate Oceanic")
    constraints.set_location("Urban with backyard")
    constraints.set_available_exercise_hours([
        ("07:00", "09:00"),  # Morning window
        ("12:00", "13:00"),  # Lunch window
        ("14:00", "18:00"),  # Afternoon window
        ("19:00", "20:30")   # Evening window
    ])
    constraints.set_weather_conditions(["Partly Cloudy", "Cool"])
    constraints.set_temperature_range(50, 65)
    constraints.set_has_yard(True)
    constraints.set_max_consecutive_activity(60)
    
    print(f"✓ Location: {constraints.get_location()}")
    print(f"✓ Climate: {constraints.get_climate()}")
    print(f"✓ Weather: {', '.join(constraints.get_weather_conditions())}")
    print(f"✓ Temperature Range: {constraints.get_temperature_range()[0]}°F - {constraints.get_temperature_range()[1]}°F")
    print(f"✓ Has Yard: {constraints.has_backyard()}")
    print(f"✓ Available Exercise Hours: {len(constraints.get_available_exercise_hours())} windows")
    
    # ========================================================================
    # STEP 5: Create Scheduler and Generate Schedule
    # ========================================================================
    print("\n⚙️ STEP 5: Creating Scheduler and Generating Schedule...")
    
    scheduler = Scheduler(owner, constraints)
    
    # Show all tasks summary
    print(scheduler.get_task_summary())
    
    # Generate optimal schedule
    print("\n📅 GENERATING OPTIMAL SCHEDULE FOR TODAY...")
    schedule = scheduler.generate_optimal_schedule("2025-03-29")
    
    # ========================================================================
    # STEP 6: Display Today's Schedule
    # ========================================================================
    print("\n" + "="*70)
    print("📆 TODAY'S SCHEDULE")
    print("="*70)
    
    schedule.display_schedule()
    
    # Display schedule in organized format
    print("\n" + "="*70)
    print("⏰ HOURLY BREAKDOWN")
    print("="*70)
    
    sorted_events = sorted(schedule.get_events(), key=lambda e: e.start_time)
    for event in sorted_events:
        duration = event.get_duration()
        print(f"\n🕐 {event.start_time} - {event.end_time} ({duration} min)")
        print(f"   📌 Task: {event.task_name}")
        print(f"   🏷️  Type: {event.event_type}")
        print(f"   ⭐ Priority: {event.priority}")
        if event.notes:
            print(f"   📝 Notes: {', '.join(event.notes)}")
    
    # ========================================================================
    # STEP 7: Display Suggestions
    # ========================================================================
    print("\n" + "="*70)
    print("💡 SYSTEM SUGGESTIONS & RECOMMENDATIONS")
    print("="*70)
    
    suggestions = scheduler.get_suggestions()
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
    else:
        print("✓ All pets' activity needs are being met!")
    
    # ========================================================================
    # STEP 8: Task Management Verification
    # ========================================================================
    print("\n" + "="*70)
    print("✅ TASK MANAGEMENT VERIFICATION")
    print("="*70)
    
    # Mark some tasks as complete
    print(f"\n✓ Marking '{task_dog1.description}' as complete...")
    task_dog1.mark_complete()
    
    print(f"✓ Marking '{task_cat1.description}' as complete...")
    task_cat1.mark_complete()
    
    # Get incomplete tasks
    incomplete_tasks = scheduler.get_all_incomplete_tasks()
    print(f"\n📊 Task Status:")
    print(f"   • Total tasks: {len(scheduler.get_all_tasks())}")
    print(f"   • Completed tasks: {len(scheduler.get_all_tasks()) - len(incomplete_tasks)}")
    print(f"   • Incomplete tasks: {len(incomplete_tasks)}")
    
    # ========================================================================
    # STEP 9: Detailed Report
    # ========================================================================
    print("\n" + "="*70)
    print("📊 DETAILED SCHEDULE REPORT")
    print("="*70)
    
    print(f"\nTotal Duration of All Tasks: {schedule.get_total_duration()} minutes")
    print(f"Wellbeing Score: {schedule.get_wellbeing_score():.2f}/1.0")
    print(f"Schedule Fully Utilized: {'Yes' if schedule.is_schedule_fully_utilized() else 'No'}")
    print(f"Number of Events: {len(schedule.get_events())}")
    
    # ========================================================================
    # STEP 10: Export Schedule
    # ========================================================================
    print("\n" + "="*70)
    print("📤 EXPORTED SCHEDULE (TEXT FORMAT)")
    print("="*70)
    print(scheduler.export_schedule('text'))
    
    # ========================================================================
    # Final Summary
    # ========================================================================
    print("\n" + "="*70)
    print("✅ TESTING COMPLETE!")
    print("="*70)
    print(f"\n✓ Successfully created {owner.get_pet_count()} pets for {owner.name}")
    print(f"✓ Generated daily schedule with {len(schedule.get_events())} events")
    print(f"✓ All pets' tasks are organized and prioritized")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
