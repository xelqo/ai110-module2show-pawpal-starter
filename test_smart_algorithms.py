"""
Test script to verify all smart algorithms work correctly.
This demonstrates the 5 smart features added in Phase 5.
"""

from pawpal_system import Owner, Pet, Task, Scheduler, Constraints, ScheduleEvent, Schedule


def test_sort_tasks_by_time():
    """Test: sort_tasks_by_time() correctly orders tasks chronologically."""
    print("\n" + "="*60)
    print("TEST 1: SORT TASKS BY TIME")
    print("="*60)
    
    owner = Owner("Alex", "alex@test.com", "555-1234", "Engineer", "owner_1")
    pet = Pet("Max", "dog", 3, 65.0, "pet_1", daily_activity_minutes=60)
    owner.add_pet(pet)
    
    # Add tasks in random order
    task1 = Task("Morning walk", "07:00", "daily", duration_minutes=30, priority="high")
    task2 = Task("Evening walk", "18:00", "daily", duration_minutes=30, priority="high")
    task3 = Task("Lunch feeding", "12:00", "daily", duration_minutes=20, priority="high")
    
    pet.add_task(task2)  # Add in wrong order
    pet.add_task(task1)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner, Constraints())
    sorted_tasks = scheduler.sort_tasks_by_time()
    
    # Verify sorting
    assert sorted_tasks[0].time == "07:00", f"Expected first task at 07:00, got {sorted_tasks[0].time}"
    assert sorted_tasks[1].time == "12:00", f"Expected second task at 12:00, got {sorted_tasks[1].time}"
    assert sorted_tasks[2].time == "18:00", f"Expected third task at 18:00, got {sorted_tasks[2].time}"
    
    print("✓ Tasks sorted correctly by time")
    for task in sorted_tasks:
        print(f"  {task.time} - {task.description}")
    return True


def test_filter_tasks_by_status():
    """Test: filter_tasks_by_status() correctly separates complete/incomplete tasks."""
    print("\n" + "="*60)
    print("TEST 2: FILTER TASKS BY STATUS")
    print("="*60)
    
    owner = Owner("Alex", "alex@test.com", "555-1234", "Engineer", "owner_1")
    pet1 = Pet("Max", "dog", 3, 65.0, "pet_1", daily_activity_minutes=60)
    pet2 = Pet("Whiskers", "cat", 2, 10.0, "pet_2", daily_activity_minutes=30)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    # Create tasks for multiple pets
    task1 = Task("Dog walk", "07:00", "daily", duration_minutes=30, priority="high")
    task2 = Task("Dog play", "15:00", "daily", duration_minutes=30, priority="high")
    task3 = Task("Cat feeding", "12:00", "daily", duration_minutes=20, priority="high")
    
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    
    # Mark some as complete
    task1.mark_complete()
    task3.mark_complete()
    
    scheduler = Scheduler(owner, Constraints())
    
    incomplete = scheduler.filter_tasks_by_status(completed=False)
    completed = scheduler.filter_tasks_by_status(completed=True)
    
    assert len(incomplete) == 1, f"Expected 1 incomplete task, got {len(incomplete)}"
    assert len(completed) == 2, f"Expected 2 completed tasks, got {len(completed)}"
    assert incomplete[0].description == "Dog play"
    
    print(f"✓ Correctly filtered {len(incomplete)} incomplete and {len(completed)} completed tasks")
    print(f"  Incomplete: {[t.description for t in incomplete]}")
    print(f"  Completed: {[t.description for t in completed]}")
    return True


def test_filter_tasks_by_pet():
    """Test: filter_tasks_by_pet() returns only tasks for specified pet."""
    print("\n" + "="*60)
    print("TEST 3: FILTER TASKS BY PET")
    print("="*60)
    
    owner = Owner("Alex", "alex@test.com", "555-1234", "Engineer", "owner_1")
    dog = Pet("Max", "dog", 3, 65.0, "pet_1", daily_activity_minutes=60)
    cat = Pet("Whiskers", "cat", 2, 10.0, "pet_2", daily_activity_minutes=30)
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Add tasks to dog
    dog_task1 = Task("Dog walk", "07:00", "daily", duration_minutes=30, priority="high")
    dog_task2 = Task("Dog play", "15:00", "daily", duration_minutes=30, priority="high")
    dog.add_task(dog_task1)
    dog.add_task(dog_task2)
    
    # Add tasks to cat
    cat_task1 = Task("Cat feeding", "08:00", "daily", duration_minutes=10, priority="high")
    cat.add_task(cat_task1)
    
    scheduler = Scheduler(owner, Constraints())
    
    dog_tasks = scheduler.filter_tasks_by_pet("Max")
    cat_tasks = scheduler.filter_tasks_by_pet("Whiskers")
    invalid_tasks = scheduler.filter_tasks_by_pet("NonExistent")
    
    assert len(dog_tasks) == 2, f"Expected 2 dog tasks, got {len(dog_tasks)}"
    assert len(cat_tasks) == 1, f"Expected 1 cat task, got {len(cat_tasks)}"
    assert len(invalid_tasks) == 0, f"Expected 0 tasks for nonexistent pet, got {len(invalid_tasks)}"
    
    print(f"✓ Correctly filtered tasks by pet")
    print(f"  Max's tasks ({len(dog_tasks)}): {[t.description for t in dog_tasks]}")
    print(f"  Whiskers's tasks ({len(cat_tasks)}): {[t.description for t in cat_tasks]}")
    return True


def test_recurring_task_automation():
    """Test: mark_task_complete() auto-creates next occurrence for recurring tasks."""
    print("\n" + "="*60)
    print("TEST 4: RECURRING TASK AUTOMATION")
    print("="*60)
    
    owner = Owner("Alex", "alex@test.com", "555-1234", "Engineer", "owner_1")
    pet = Pet("Max", "dog", 3, 65.0, "pet_1", daily_activity_minutes=60)
    owner.add_pet(pet)
    
    # Create a daily recurring task
    daily_task = Task("Morning walk", "07:00", "daily", duration_minutes=30, priority="high")
    pet.add_task(daily_task)
    
    initial_count = len(pet.get_tasks())
    assert initial_count == 1, f"Expected 1 task initially, got {initial_count}"
    
    scheduler = Scheduler(owner, Constraints())
    
    # Mark as complete (should create new occurrence)
    scheduler.mark_task_complete("Max", "Morning walk")
    
    final_count = len(pet.get_tasks())
    assert final_count == 2, f"Expected 2 tasks after completion, got {final_count}"
    
    # Verify the original is marked complete
    completed_tasks = [t for t in pet.get_tasks() if t.is_complete()]
    assert len(completed_tasks) == 1, f"Expected 1 completed task, got {len(completed_tasks)}"
    
    # Verify new task was created
    incomplete_tasks = [t for t in pet.get_tasks() if not t.is_complete()]
    assert len(incomplete_tasks) == 1, f"Expected 1 incomplete task, got {len(incomplete_tasks)}"
    assert incomplete_tasks[0].time == "07:00", "New task should have same time"
    assert incomplete_tasks[0].frequency == "daily", "New task should have same frequency"
    
    print(f"✓ Recurring task auto-created successfully")
    print(f"  Initial tasks: {initial_count}")
    print(f"  Final tasks: {final_count}")
    print(f"  Original task status: Complete")
    print(f"  New task created: True")
    return True


def test_conflict_detection():
    """Test: check_conflicts() detects overlapping task durations."""
    print("\n" + "="*60)
    print("TEST 5: CONFLICT DETECTION")
    print("="*60)
    
    schedule = Schedule("2025-03-29")
    
    # Create two events that DON'T overlap
    event1 = ScheduleEvent(
        task_name="Morning walk",
        start_time="07:00",
        end_time="07:30",
        location="Park",
        event_type="task",
        priority="high"
    )
    
    event2 = ScheduleEvent(
        task_name="Breakfast",
        start_time="07:30",
        end_time="07:50",
        location="Home",
        event_type="task",
        priority="high"
    )
    
    event3 = ScheduleEvent(
        task_name="Evening walk",
        start_time="18:00",
        end_time="18:45",
        location="Park",
        event_type="task",
        priority="high"
    )
    
    schedule.add_event(event1)
    schedule.add_event(event2)
    schedule.add_event(event3)
    
    owner = Owner("Alex", "alex@test.com", "555-1234", "Engineer", "owner_1")
    scheduler = Scheduler(owner, Constraints())
    scheduler.schedule = schedule
    
    conflicts = scheduler.check_conflicts()
    assert len(conflicts) == 0, f"Expected no conflicts, got {len(conflicts)}"
    
    print(f"✓ Correctly detected no conflicts in 3-event schedule")
    print(f"  Events: {len(schedule.get_events())}")
    print(f"  Conflicts: {len(conflicts)}")
    
    # Now test the is_conflicting method directly
    overlap1 = ScheduleEvent(
        task_name="Walk",
        start_time="07:00",
        end_time="07:30",
        location="Park",
        event_type="task",
        priority="high"
    )
    
    overlap2 = ScheduleEvent(
        task_name="Feeding",
        start_time="07:15",
        end_time="07:40",
        location="Home",
        event_type="task",
        priority="high"
    )
    
    # Test the is_conflicting method
    has_conflict = overlap1.is_conflicting(overlap2)
    assert has_conflict, "Expected these events to conflict"
    
    print(f"\n✓ Correctly detected conflicts using is_conflicting()")
    print(f"  Event 1: 07:00-07:30")
    print(f"  Event 2: 07:15-07:40")
    print(f"  Conflict detected: {has_conflict}")
    
    # Also test adjacent events (no conflict)
    adjacent1 = ScheduleEvent(
        task_name="Event1",
        start_time="08:00",
        end_time="08:30",
        location="Home",
        event_type="task",
        priority="high"
    )
    
    adjacent2 = ScheduleEvent(
        task_name="Event2",
        start_time="08:30",
        end_time="09:00",
        location="Home",
        event_type="task",
        priority="high"
    )
    
    no_conflict = adjacent1.is_conflicting(adjacent2)
    assert not no_conflict, "Expected adjacent events to not conflict"
    
    print(f"\n✓ Correctly identified adjacent events as non-conflicting")
    print(f"  Event 1: 08:00-08:30")
    print(f"  Event 2: 08:30-09:00")
    print(f"  Conflict detected: {no_conflict}")
    
    return True


def run_all_tests():
    """Run all algorithm tests."""
    print("\n" + "="*60)
    print("🧠 SMART ALGORITHM TEST SUITE")
    print("="*60)
    
    tests = [
        ("Sort Tasks by Time", test_sort_tasks_by_time),
        ("Filter Tasks by Status", test_filter_tasks_by_status),
        ("Filter Tasks by Pet", test_filter_tasks_by_pet),
        ("Recurring Task Automation", test_recurring_task_automation),
        ("Conflict Detection", test_conflict_detection),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, "PASS" if result else "FAIL"))
        except AssertionError as e:
            print(f"\n✗ TEST FAILED: {e}")
            results.append((name, "FAIL"))
        except Exception as e:
            print(f"\n✗ ERROR: {e}")
            results.append((name, "ERROR"))
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for name, result in results:
        status_icon = "✓" if result == "PASS" else "✗"
        print(f"{status_icon} {name}: {result}")
    
    passed = sum(1 for _, r in results if r == "PASS")
    total = len(results)
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
