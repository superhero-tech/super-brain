# Fixture: Re-run - Scope Change

## Scenario

The user has an existing about.md (filled in 3 months ago). Their role changed - they went from solo founder to PM at a large company. They want to update the profile.

## Pre-condition

Before running the skill, `8-System/about.md` contains:

```markdown
# About me

> This file tells your AI who you are, how you work and what you expect from it.
> Fill it in by running the `second-brain-setup` skill, or edit it by hand.

---

## Context

Solo founder building a SaaS for contract management aimed at small law firms. 12 beta users, zero revenue. Firms need something simpler than the enterprise contract suites, more professional than Excel. Competition = Excel and Word. Key metric: weekly retention.

## How to work with me

- Talk to me bluntly and hard. Do not soften criticism.
- Structure your answers - bullets, frames, step by step.
- Keep it short. Bottom line first, details only if I ask.
- Dry, direct tone, no ceremony.
- Push me out of my comfort zone. Do not let me coast.
- Push me on: Execution and Delivery, Analytics and Data.
- I tend to build features instead of measuring what works - remind me about the data.

## Current goal

Get to 50 paying users and validate the business in 4 months.

---

## History

- 2026-01-15: profile created (interview)
```

## Inputs

### Reaction to the AI's summary

> I changed jobs. I shut the SaaS down - it did not validate. I am a PM at a large retail bank now, a team of 8, we work on the mobile app for retail customers. Communication style and the rest stay as they are.

### Confirmation

> Save

## Expected output

### Structural assertions

- [ ] File written to `8-System/about.md`
- [ ] Contains all four sections (Context, How to work with me, Current goal, History)
- [ ] History contains BOTH the old entry (2026-01-15) AND a new entry with today's date

### Content assertions - Context

- [ ] Updated: contains "PM", "retail bank", "mobile app" and "retail customers"
- [ ] Does NOT contain the old SaaS/law-firm information (replaced, not appended)
- [ ] Contains "team of 8" or equivalent

### Content assertions - How to work with me

- [ ] UNCHANGED or minimally changed. The user said "stay as they are" - the AI should not rewrite it
- [ ] The communication-style bullets are preserved (blunt, structured, short, dry, demanding)
- [ ] The development areas are preserved (Execution, Analytics)

### Content assertions - Current goal

- [ ] Updated - the old goal (50 users, validation) makes no sense in the new context
- [ ] The AI should have asked for a new goal OR proposed a placeholder
- [ ] If the AI proposed a goal, it has to be consistent with the new role

### Content assertions - History

- [ ] Contains: `- 2026-01-15: profile created (interview)`
- [ ] Contains a new entry with today's date noting "updated Context" (or equivalent)
- [ ] The old entry was NOT deleted or modified

### Flow assertions

- [ ] The AI started by summarising the existing profile ("I already know you a bit...")
- [ ] The AI did NOT ask the full Q1-Q4 question set
- [ ] The AI asked only about the delta
- [ ] The AI asked about the new goal (the old one does not fit the new context)
- [ ] The proposal was shown before writing

### Red flags

- [ ] The AI asked every question again (Q1, Q2, Q3, Q4)
- [ ] The AI deleted old History entries
- [ ] The AI rewrote "How to work with me" even though the user said it stays
- [ ] The AI wrote the file without a proposal and confirmation
- [ ] The AI modified brain.md
