# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling Features

PawPal+ includes intelligent algorithms that make the scheduling system more efficient and user-friendly:

### 1. Smart Task Sorting
The `sort_tasks_by_time()` method uses a time-to-minutes conversion algorithm to organize tasks chronologically. Tasks are parsed from "HH:MM" format and sorted by their minutes since midnight, enabling chronological ordering of any task set.

### 2. Task Filtering
Two powerful filtering methods help users find what they need:
- `filter_tasks_by_status()`: Returns only completed or incomplete tasks across all pets
- `filter_tasks_by_pet()`: Retrieves all tasks for a specific pet by name

### 3. Recurring Task Automation
When a recurring task (daily or weekly) is marked complete via `mark_task_complete()`, the system automatically creates a new task instance for the next occurrence. This eliminates manual re-entry of routine activities.

### 4. Conflict Detection
The `ScheduleEvent.is_conflicting()` method detects overlapping task durations (not just exact time matches). The scheduler checks all event pairs and returns detailed warnings about conflicts, helping prevent scheduling collisions.

### 5. Optimization Suggestions
The `get_suggestions()` method analyzes the schedule to identify:
- Pets not receiving adequate exercise minutes
- Incomplete high-priority tasks
- Schedule utilization opportunities

### Testing the Algorithms

Run `python main.py` to see all algorithms in action:
- Tasks are sorted by time for easy reading
- Tasks are filtered by status and by pet
- Recurring tasks auto-create after completion
- Conflict detection validates the schedule

## Testing PawPal+

The PawPal+ system includes a comprehensive test suite that validates all core functionality, smart algorithms, and integration scenarios.

### Running Tests

To run the complete test suite:

```bash
python -m pytest tests/test_pawpal.py -v
```

To run tests with coverage information:

```bash
python -m pytest tests/test_pawpal.py --cov=pawpal_system --cov-report=html
```

To run a specific test class:

```bash
python -m pytest tests/test_pawpal.py::TestScheduler -v
```

### Test Coverage

The test suite includes **30 comprehensive tests** organized into 6 test classes:

#### 1. **Task Tests** (3 tests)
- Task creation with all attributes
- Completion status changes (mark_complete, mark_incomplete)
- String representation formatting

#### 2. **Pet Tests** (4 tests)
- Pet creation and initialization
- Task addition and task counting
- Incomplete vs. completed task tracking
- Task removal functionality

#### 3. **Owner Tests** (3 tests)
- Owner creation with contact information
- Pet addition and pet counting
- Pet retrieval by name

#### 4. **Schedule Tests** (7 tests)
- ScheduleEvent creation and attributes
- Event duration calculation
- Conflict detection (overlapping events)
- Non-conflicting events
- Schedule creation and event management
- Conflict prevention in schedule

#### 5. **Scheduler Tests** (3 tests)
- Scheduler initialization
- Optimal schedule generation
- Retrieval of all tasks across pets

#### 6. **Smart Algorithm Tests** (9 tests)
- **Sorting**: Tasks arranged chronologically by time
- **Sorting Edge Case**: Empty task lists handled correctly
- **Filtering by Status**: Complete vs. incomplete task separation
- **Filtering by Pet**: Tasks isolated by pet ownership
- **Recurring Tasks (Daily)**: Auto-creation of next daily occurrence
- **Recurring Tasks (Weekly)**: Auto-creation of next weekly occurrence
- **Conflict Detection**: Multiple events without conflicts
- **Edge Case (Single Task)**: System behavior with minimal data
- **Edge Case (Same Time)**: Multiple pets at same scheduled time

#### 7. **Integration Tests** (1 test)
- Complete workflow: owner → pets → tasks → schedule → completion

### Test Results

```
30 passed in 0.04s
```

✅ **100% Test Pass Rate** - All core behaviors verified

### Edge Cases Tested

The test suite thoroughly validates edge cases that commonly cause issues:

- **Empty collections**: Single pet with no tasks, single pet with single task
- **Time conflicts**: Multiple events at the same time from different pets
- **Status filtering**: Multiple pets with mixed task completion states
- **Recurring tasks**: Both daily and weekly frequency types
- **Task removal**: Proper cleanup of pet task lists
- **Pet lookup**: Retrieving existing vs. non-existent pets

### Confidence Level

Based on comprehensive test coverage and successful execution of 30 tests:

**⭐⭐⭐⭐⭐ 5/5 Stars** - High Confidence in System Reliability

The PawPal+ system demonstrates robust handling of:
- Core data model operations (CRUD)
- Complex scheduling logic
- Smart algorithms (sorting, filtering, conflict detection)
- Multi-pet owner scenarios
- Edge cases and error conditions

The system is production-ready for scheduling pet care tasks with confidence in correctness, maintainability, and reliability.

