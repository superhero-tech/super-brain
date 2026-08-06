---
name: second-brain-setup
description: Use when creating or refreshing a product builder's personal profile in 8-System/about.md - supports both assessment-based (Gallup, DISC, MBTI) and interview-based onboarding
---

# Second Brain Setup

## Purpose

Runs a conversation with the product builder and writes the result to `8-System/about.md`. That file tells the agent who the human is, how they want to be treated and where they need to be pushed. It works as a pair with `8-System/brain.md`, which holds the universal operating rules.

## When to use

- Setting up a new vault for the first time
- Refreshing the profile after a role change, a new project or a shift in priorities
- When the AI feels "out of calibration"

## How it works

### Step 0: Pick a path

Ask:

> There are two ways for me to get to know you:
>
> **A) I have assessment results** - paste your CliftonStrengths (Gallup), DISC, MBTI, 16Personalities, Enneagram, Working Genius or any other personality/competency assessment. I will pull out the parts that change how we work together.
>
> **B) Let's talk** - I will run a short interview (5-7 minutes).
>
> You can do both: start with the assessment, then fill the gaps by talking.

### Path A: Assessment-first

1. Read the pasted results
2. Extract ONLY operational information - the parts that change how the AI works:
   - Strengths -> how the AI should frame recommendations
   - Weaknesses and blind spots -> where the AI should actively push
   - Communication style -> how the AI should speak
   - Decision style -> how the AI should present options
3. Do NOT copy the full report into `about.md`. The extract is 5-8 bullets in the "How to work with me" section
4. Ask short follow-up questions about what the assessment does not cover:
   - Current role and context (Q1 from `references/questions.md` - short version, 2-3 sentences is enough)
   - Six-month goal (Q4 from `references/questions.md`)
5. Go to Step 3 (proposal)

### Path B: Interview

1. Ask the questions in `references/questions.md` in order: Q1 (Context), Q2 (Communication style), Q3 (Development areas), Q4 (Goals)
2. Rules:
   - Q1: all six sub-questions in one block, one answer
   - Q2.1-Q2.5: five multiple-choice questions, one at a time
   - Q3: multi-select, 2-3 from a list of 8
   - Q4: one open question
3. Go to Step 3 (proposal)

### Step 3: Propose the content of about.md

**Do not write the file yet.** Show the full proposal:

> Here is what I want to write to `8-System/about.md`:
>
> ```
> [full file content]
> ```
>
> Look right? Say "save" or tell me what to fix.

File format - three sections:

```markdown
# About me

## Context
[Role, company, product, users, metrics - from Q1 or from the assessment plus follow-up]

## How to work with me
[5-8 bullets: communication style, strengths, blind spots, how to frame recommendations]
[Path A: extract from the assessment. Path B: from Q2 + Q3]

## Current goal
[From Q4, in their own words]

---
## History
- [YYYY-MM-DD]: profile created [path A: based on CliftonStrengths / path B: interview]
```

### Step 4: Save after confirmation

Only after an explicit "save", "OK", "yes" - write to `8-System/about.md`. Append an entry to History.

### Re-run mode

When `about.md` already exists:

1. Read the existing file
2. Summarise it: "I already know you a bit. Your current profile says..."
3. Ask: "What changed?"
4. Update only the delta
5. Append a history entry: `- [YYYY-MM-DD]: updated [list of sections]`

## STOP - red flags

- Writing `about.md` without showing a proposal and getting confirmation
- Modifying `brain.md` (never allowed)
- Copying a full Gallup/DISC report into `about.md` instead of an operational extract
- In re-run mode, asking everything again instead of asking for the delta
- Asking the user to pick their role from a closed list of job titles
- Implying that some roles are "more of a product builder" than others

## References

- `references/questions.md` - the full question set with multiple-choice options
