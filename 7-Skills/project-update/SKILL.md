---
name: project-update
description: Records what happened in a project as an artefact, a log entry and a refreshed index row. Use when the human reports progress, a decision, a prototype or a result, or when a project's scope has moved.
---

# Project Update

Turn "here is what happened this week" into project state someone can pick up cold in three months.

Write every file in the language the human is using.

## How to invoke

- "I have an update", "here is what happened", "update the project"
- The human reports a decision, a prototype, a test result or a piece of research
- The scope of a project has moved

## How it works

### 1. Orient before you write

Read, in this order:

1. `3-Projects/index.md` - which projects exist and which one this is about
2. `<project>/brief.md` - what it was meant to be
3. `<project>/rules.md` - constraints that override your defaults here
4. The top five entries of `<project>/log.md` - what it has actually become

The brief and the log answer different questions. Skipping the log is how you give advice that was already tried and rejected two weeks ago.

If the human has not said which project, ask. Guessing from the topic puts work in the wrong folder.

### 2. Ask for what is missing

Most updates arrive as one sentence. The three questions that turn it into something durable:

- What did you decide?
- What did you build or test?
- What did you learn?

Ask only about the gaps. An update that already says what changed and why does not need an interview.

### 3. Write the artefact

Route by what actually happened:

| What happened | Where it goes |
|---|---|
| A decision | `<project>/decisions/`, using `6-Templates/decision-record.md` |
| Something built | `<project>/prototypes/` - link, screenshots, spec |
| A result or a learning | `<project>/analyses/` |
| Interviews, data, hypotheses | `<project>/discovery/` |

File names start with the date: `2026-03-14-drop-templates.md`.

Everything stays inside the project folder. Project work does not go to `9-Outputs/` or the vault root.

### 4. Log it

Append an entry to `<project>/log.md`, newest at the top. The entry format and the list of valid types are in `3-Projects/README.md` - read it if you have not this session.

Two fields carry the weight: **what changed** and **why**. An entry without a why is a changelog, and a changelog does not help anyone decide anything later. Point **Files** at the artefact you just wrote; the log summarises, it never becomes the artefact.

Never edit or delete an existing entry. Corrections are a new entry that says what was wrong.

### 5. Refresh the index

Update the project's row in `3-Projects/index.md`: the status if it moved, and the last-update cell with the date and headline of the entry you just wrote.

This is the step that decays first and costs the most. A stale index means the next session starts from a false picture of what is live.

### 6. Check the brief

If the scope, the audience or the definition of done has moved, say so and offer to update `brief.md`. Show the change and wait - the human owns that file.

### 7. Check whether this is bigger than the project

Some learnings are not about this project at all. "Marketplaces behave differently than I assumed" is general knowledge that will outlive the work it came from.

When that happens, offer to add it to `4-Knowledge/` as a wiki page. Say what you would write and let the human decide.

## Self-check

- The artefact is on disk, in the right subfolder, with a dated file name
- `<project>/log.md` has a new entry at the top, with a why and a link to the artefact
- The project's row in `3-Projects/index.md` matches that entry
- Anything that outgrew the project was offered to Knowledge

## Hard constraints

- `rules.md` is the human's file. Suggest additions, wait for a yes.
- `brief.md` changes only after the human sees the change and agrees.
- Log entries are append-only.
- Project outputs stay inside the project folder.
