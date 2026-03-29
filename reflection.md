# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
The UML design should be able to have basic pet info input, personalized tasks for each pet and subseqeunt priority establishment of the tasks. The user should then get a detailed schedule thats easy to follow and be given reasoning on why the schedule makes sense, mainly accounting for and adhearing to all the constraints.

I would include am Owner, Pet, constraints, Task, and Scheduler classes. The pet and owner info is just basic info, constraints are the specific constraints like there is snow or walks can only happen at certain times. Tasks are the things that need to happen for the pet every day. Scheduler takes account for all of this and is responseible for using the constraints and tasks to map the most optimal schedule while also providing reasoning. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
I had a empty sketon with a lot of the functions being just passed but after going back was able to implement alot of the logic after asking for real implementations. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

### Tradeoff: Exact Time Matching vs. Overlapping Duration Detection

The conflict detection algorithm uses `is_conflicting()` which checks if two events have overlapping durations. This is more sophisticated than checking exact start times, but it still makes a simplifying assumption: **it does not account for transition time between tasks**.

**The tradeoff:**
- **What we do:** Check if event end_time <= other_event start_time (no overlap = no conflict)
- **What we don't do:** Add buffer time (e.g., 5 minutes to transition between tasks or locations)

**Why it's reasonable:**
1. **Simplicity:** For a pet owner with a single location (home), most tasks don't require travel time
2. **User control:** The owner can manually add buffer tasks if needed ("transition time", "travel to park")
3. **Task duration accuracy:** The 30-minute "Morning Walk" already includes realistic time for the activity
4. **Functionality:** We prevent actual scheduling collisions (two tasks at 07:00-07:30 and 07:15-08:00), which is the critical case

**Trade-off decision:** We chose correctness for the most common case (no overlaps) over edge cases (transition time). In production, we could add an optional "buffer_minutes" parameter to tasks or a global setting for travel time.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

The comprehensive test suite includes 30 tests covering:

1. **Core Data Model Operations (10 tests):**
   - Task creation, completion status, string representation
   - Pet creation, task management, incomplete task tracking
   - Owner creation, pet management, pet lookup

2. **Scheduling and Conflict Detection (7 tests):**
   - ScheduleEvent creation and attributes
   - Event duration calculation
   - Conflict detection for overlapping events
   - Schedule creation and conflict prevention

3. **Smart Algorithms (9 tests):**
   - Task sorting by chronological time
   - Task filtering by completion status
   - Task filtering by pet ownership
   - Recurring task auto-creation (daily and weekly)
   - Conflict detection with multiple events
   - Edge cases: empty lists, single tasks, same times across pets

4. **Integration Tests (1 test):**
   - Complete workflow: create owner → add pets → add tasks → generate schedule → mark complete

**Why these tests were important:**

- **Sorting correctness** ensures users see tasks in the right order (07:00 before 14:00)
- **Filtering** validates that data isolation works (only Max's tasks, not Whiskers')
- **Recurring tasks** confirm automation eliminates manual re-entry
- **Conflict detection** prevents impossible schedules (two tasks at 07:00-07:30)
- **Edge cases** catch bugs in empty/minimal datasets
- **Integration** validates the entire system works end-to-end

**b. Confidence**

**Confidence Level: ⭐⭐⭐⭐⭐ 5/5 Stars**

**Why high confidence:**

1. **100% test pass rate** - All 30 tests pass without failures
2. **Comprehensive coverage** - All 5 smart algorithms verified
3. **Edge case validation** - Empty lists, single items, same-time tasks tested
4. **Multi-pet scenarios** - Cross-pet filtering and scheduling validated
5. **Recurring logic** - Both daily and weekly tasks auto-create correctly
6. **Conflict prevention** - Schedule prevents impossible time overlaps

**Edge cases tested successfully:**

- Empty task list (sorting returns empty list)
- Single task (system handles minimal data)
- Same time, different pets (correctly schedules both)
- Task completion state changes (proper tracking)
- Pet lookup with non-existent pets (returns None safely)

**Edge cases I would test next with more time:**

1. **Extreme times:** Tasks at 23:59 or tasks spanning midnight
2. **Rapid operations:** Marking same task complete twice
3. **Concurrent pets:** 10+ pets with overlapping schedules
4. **Year boundaries:** Tasks spanning Dec 31 to Jan 1
5. **Constraint violations:** Tasks that violate owner availability
6. **Performance:** Sorting/filtering with 1000+ tasks
7. **UI edge cases:** Invalid time formats ("25:00", "12:60")
8. **Data corruption:** Recovering from incomplete owner/pet records

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
