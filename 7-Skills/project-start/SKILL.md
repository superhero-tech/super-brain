---
name: project-start
description: Sets up a new project folder and runs the interview that fills its brief. Use when the human starts a new project, or when work that has been living in chat needs a home with a brief, rules and a log.
---

# Project Start

Copying three files takes a second. The value of this skill is the conversation that fills them, because a brief nobody pushed back on says "for all users" and "success is more engagement" and helps no one.

Run the interview in the language the human is using.

## How to invoke

- "New project", "let's start a project on X"
- Work that has been living in the chat needs a folder
- `/project-start`

## How it works

### 1. Name it

Get the project name, and derive a kebab-case slug: `contract-tracker`, `q3-pricing`.

Check `3-Projects/` for a folder with that slug. If it exists, this is an update to an existing project, not a new one - say so and stop.

### 2. Create the folder

Copy `3-Projects/_template/` to `3-Projects/<slug>/`, then create the four working subfolders: `discovery/`, `decisions/`, `prototypes/`, `analyses/`.

Do not fill in the brief yet.

### 3. Check what the vault already knows

Read `4-Knowledge/index.md` and look for pages that bear on this domain. If there are any, name them:

> Before we start: the wiki already has [[Page A]] and [[Page B]] on this. Want me to link them from the brief so you are not starting from zero?

This is the payoff for every source ever ingested. On an empty wiki, skip it without comment.

### 4. Run the brief interview

One question at a time, in this order. Do not paste the whole template and ask them to fill it in.

| Section | What you are asking for | Push back when |
|---|---|---|
| In one sentence | What it does and for whom | It needs an "and" to hold two ideas - that is usually two projects |
| Who it is for | A segment they could go and find tomorrow | The answer is "everyone", "users", "SMBs" - ask who the first ten would be |
| What done looks like | An outcome with a number and a date | The answer is a direction. "More engagement" is not an outcome; "50 paying by end of Q2, or we stop" is |
| Context | Why this project, why now | It reads as a feature description rather than a reason |
| Constraints | What is genuinely non-negotiable: money, deadline, people, tech, legal | Everything is listed as a constraint, which means nothing is |
| Open questions | What they do not know yet | The list is empty on day one, which means the project has not been thought about |

Push back once per section, not three times. If the honest answer is "I do not know yet", that is a real answer: write it into Open questions and move on. A brief with holes that names its holes beats a project with no folder.

### 5. Show the draft, then write

Show the filled brief in the conversation and wait for a yes before saving it. The human owns `brief.md`.

### 6. Ask about rules

Ask what constraints apply to this project specifically - things that should override the agent's normal behaviour. Most projects start with none.

When there are none, write an explicit "None yet." under each heading in `rules.md`. An empty file reads as "no contract here"; an explicit "None yet." reads as "asked and answered".

### 7. Register it

- Add the row to `3-Projects/index.md`: status `active`, the In-one-sentence line, today's date. The row format is in `3-Projects/README.md`.
- Write the first entry in `<slug>/log.md`: type `scope-change`, what changed is that the project exists, why is the reason they just gave you in Context.

## Self-check

- The slug did not already exist
- `brief.md` was shown and agreed before it was written
- Every section holds something specific, or names itself as an open question
- `rules.md` says "None yet." rather than sitting empty
- `3-Projects/index.md` has the row and `log.md` has the first entry

## Hard constraints

- The brief is written after the human agrees to it, never from your own assumptions.
- A section they could not answer becomes an open question. Filling it in yourself produces a brief that looks finished and means nothing.
- The four working subfolders are created empty. Work goes in them later, not at setup.
