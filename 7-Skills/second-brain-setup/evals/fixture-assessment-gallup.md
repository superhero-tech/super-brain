# Fixture: Assessment Path - Gallup CliftonStrengths

## Scenario

The user picks Path A and pastes their Gallup Top 5 results.

## Inputs

### Step 0: Path choice

> A

### Pasted results

> My Top 5 CliftonStrengths:
> 1. Strategic - I see patterns and alternative routes, I evaluate scenarios fast
> 2. Achiever - I need to get something measurable done every day, internal drive to act
> 3. Ideation - I am fascinated by connections between seemingly unrelated concepts
> 4. Command - natural pull toward taking control, confronting, saying things plainly
> 5. Activator - impatient with planning that has no action, I want to start immediately
>
> My Bottom 5:
> 34. Discipline - chaotic about organisation, struggle with routines and systems
> 33. Consistency - I do not like treating everyone the same, I look for exceptions
> 32. Deliberative - I decide fast, sometimes too fast
> 31. Harmony - I do not avoid conflict, I go looking for it when I see a problem
> 30. Analytical - I prefer intuition and patterns over detailed data analysis

### Follow-up: Context (short version)

> PM at a fintech startup, 30 people, we are building a neobank for freelancers. The market is growing but regulation slows us down.

### Follow-up: Goal

> Ship the MVP by the end of Q3 and close the seed round.

### Confirmation

> Save

## Expected output

### Structural assertions

- [ ] File written to `8-System/about.md`
- [ ] Contains the heading `# About me`
- [ ] Contains the sections `## Context`, `## How to work with me`, `## Current goal`, `## History`
- [ ] The History section contains a dated entry noting "based on CliftonStrengths"

### Content assertions - Context

- [ ] Contains "PM", "fintech", "neobank" and "freelancers"
- [ ] Contains company size (~30 people) and stage (startup)
- [ ] Does NOT contain the full list of 34 strengths - this is an extract, not a report

### Content assertions - How to work with me

- [ ] Contains 5-8 bullets (no fewer than 5, no more than 8)
- [ ] At least one bullet references the strengths (Strategic/Ideation/Command)
- [ ] At least one bullet references the blind spots (Discipline/Deliberative)
- [ ] At least one bullet is an operational instruction for the AI (e.g. "remind me to be systematic", "make me look at the data before I decide")
- [ ] It is NOT a transcribed Gallup report - it is an operational extract
- [ ] The bullets are specific and actionable, not generic

### Content assertions - Current goal

- [ ] Contains "MVP", "Q3" and "seed round" (or synonyms)

### Red flags (the test fails if any of these is true)

- [ ] The AI wrote the file without showing a proposal and getting confirmation
- [ ] The AI copied the full Gallup report (all 34 entries) into about.md
- [ ] The AI modified brain.md
- [ ] The AI asked the full Q1-Q4 question set even though the user picked Path A
- [ ] The "How to work with me" section has fewer than 5 bullets
