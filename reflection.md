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

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
