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
