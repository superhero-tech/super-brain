# Projects - Agent Instructions

One folder per project. Folder name is a kebab-case slug: `contract-tracker`, `q3-pricing`, `mobile-onboarding`.

This folder exists so that an agent joining a project cold can answer three questions in under a minute:
**what is this project, what rules apply to it, and what changed most recently.**

---

## Read before you touch anything

In this order, every time:

1. **`3-Projects/index.md`** - one row per project. Tells you which projects exist, which are active, and what each one is about.
2. **`<project>/brief.md`** - what the project is, who it is for, what "done" looks like.
3. **`<project>/rules.md`** - constraints that apply to this project only. These override your defaults.
4. **`<project>/log.md`** - reverse-chronological history. Read the top 5 entries. That is the recent state.

Do not start work from `brief.md` alone. The brief is what the project was supposed to be; the log is what it has become.

If a project folder is missing `rules.md` or `log.md`, say so and offer to create them from `_template/`.

---

## Who owns what

| File | Owner | Rule |
|---|---|---|
| `index.md` | **AI** | Refresh the project's row at the end of any session that changed the project |
| `<project>/brief.md` | Human | The AI proposes edits, the human approves. Never rewrite it silently. |
| `<project>/rules.md` | Human | The AI never edits this without explicit permission. It may suggest additions. |
| `<project>/log.md` | **AI** | Append-only. Newest entry at the top. Never edit or delete an old entry. |
| `decisions/`, `prototypes/`, `analyses/`, `discovery/` | AI writes, human reads | Everything the project produces lands here, never at vault root |

---

## `index.md` - the project index

One row per project. Keep it to one line each - this file is read on every project session, so it has to stay cheap to read.

```markdown
| Project | Status | What it is | Last update |
|---|---|---|---|
| [contract-tracker](contract-tracker/) | active | SaaS for small law firms, validating weekly retention | 2026-03-14 - killed the templates feature |
```

- **Status**: `active`, `paused`, `shipped`, `killed`. Nothing else.
- **What it is**: one sentence. What it does and for whom. Not a mission statement.
- **Last update**: the date and headline of the newest `log.md` entry, copied verbatim.

Update the row when: a project is created, its status changes, or you append a log entry. Sort active projects to the top.

Never invent a row for a folder you have not read. If `index.md` and the folders on disk disagree, say so and ask - do not quietly reconcile.

---

## `log.md` - the project log

Append-only, newest first. This is the file that tells the next agent what actually happened.

```markdown
## 2026-03-14 - Killed the templates feature

**Type:** decision
**What changed:** Dropped templates from scope. Focusing the next two weeks on the import flow instead.
**Why:** 3 of 5 beta users never opened templates. Import came up unprompted in 4 of 5 interviews.
**Next:** Ship the CSV import behind a flag, measure weekly active use.
**Files:** `decisions/2026-03-14-drop-templates.md`, `discovery/interviews-beta-round-2.md`
```

- **Type** is one of: `decision`, `prototype`, `analysis`, `research`, `scope-change`, `shipped`.
- **What changed** and **Why** are mandatory. An entry without a "why" is a changelog, not a log.
- **Files** points at the artefacts. The log summarises; it never becomes the artefact.
- Keep entries short. If it takes more than six lines, the detail belongs in a file under `decisions/` or `analyses/`.

Write an entry when: a decision is made, something is built or tested, research lands, or the scope moves. Do not log "worked on the project".

---

## Starting a new project

**Run the `project-start` skill.** It creates the folder from `_template/`, interviews the human to fill `brief.md`, asks what rules apply, registers the project in `index.md` and writes the first log entry.

The interview is the point. A brief nobody pushed back on says "for all users" and "success is more engagement", and a project that starts there stays there.

---

## STOP - red flags

- Starting project work without reading `index.md`, `brief.md`, `rules.md` and the top of `log.md`
- Editing or deleting an existing `log.md` entry instead of appending a new one
- Editing `rules.md` without being asked
- Rewriting `brief.md` without showing the change and getting a yes
- Writing project outputs outside the project folder
- Adding an `index.md` row for a project that does not exist on disk
