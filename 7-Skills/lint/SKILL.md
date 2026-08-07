---
name: lint
description: Health check over the compiled wiki in 4-Knowledge/, written up as a ranked report. Use when the human asks to check or lint the wiki, on the monthly maintenance pass, or before the vault gets trusted on a decision that matters.
---

# Lint

Find what has rotted in the wiki, rank it, and hand the list to the human. Fixing is a separate decision.

Write the report in the language the wiki is written in.

## How to invoke

- "Check the wiki", "run a lint", "health check"
- The monthly maintenance pass
- Before the human leans on the vault for something expensive

## What this catches, and what it does not

Structural problems - missing citations, orphans, index drift, stale pages - it finds reliably, because they are mechanical.

Reasoning errors it finds badly. The model running this check shares its blind spots with the model that wrote the pages, so a clean report means the wiki is tidy, not that it is right. Say this out loud when you hand over a report with no errors. `8-System/limits.md` has the longer version.

## How it works

### 1. Decide whether there is anything to check

Count the pages in `4-Knowledge/`. Under ten, say there is not enough wiki to lint yet and stop. An empty report trains the human to ignore the next one.

### 2. Read everything

Read `4-Knowledge/index.md`, then every wiki page. This is the one workflow that does not get to work from the index alone.

### 3. Classify what you find

| Severity | What to look for |
|---|---|
| `ERROR` | Two pages that contradict each other |
| `ERROR` | Claims with no `[source: ...]` citation |
| `ERROR` | Index entries pointing at pages that do not exist, or pages missing from the index |
| `WARN` | Orphan pages - nothing links to them |
| `WARN` | Pages marked `status: needs_update`, or with `last_updated` older than six months |
| `WARN` | Pages with `source_count: 1` that assert more than one source can carry |
| `INFO` | Concepts mentioned across several pages with no page of their own |
| `INFO` | People, companies or tools named on three or more pages with no entity page |
| `INFO` | Entity pages longer than the concept pages they point at - the argument is in the wrong place |
| `INFO` | Connections worth making between existing pages |

Every finding names the page and says what to do about it. "Page X has issues" is not a finding.

### 4. Write the report

Save it to `4-Knowledge/lint-[YYYY-MM-DD].md`:

```markdown
---
title: Lint report
created: [YYYY-MM-DD]
pages_checked: [n]
---

# Lint report - [YYYY-MM-DD]

Checked [n] pages. Found [x] errors, [y] warnings, [z] notes.

## ERROR

- **[[Page Name]]** - contradicts [[Other Page]] on [claim]. `[source-a.md]` says X,
  `[source-b.md]` says Y. Neither is flagged.

## WARN

- **[[Page Name]]** - orphan, nothing links here. Closest candidates: [[A]], [[B]]

## INFO

- "[concept]" appears on 4 pages and has none of its own. Worth writing.
- "[person or company]" is cited on 5 pages with no entity page. It has become a hub
  without one.

## Suggested next

1. [The single most valuable fix]
2. [Then this]
3. [Then this]
```

Rank the suggestions by what they unblock, not by severity order. An unranked report gets read once and never again.

### 5. Log it

Append a `lint` entry to `4-Knowledge/log.md`. That file carries the format.

### 6. Hand it over

Report the counts and the top suggestion in the conversation, then stop. The human decides what gets fixed.

If they say go ahead, the fixes are a separate pass: make them, append an `update` entry to `4-Knowledge/log.md` saying which pages changed and why, and refresh `4-Knowledge/index.md` if any page description moved.

## Self-check

- Every finding names a page and a next action
- The report is on disk at `4-Knowledge/lint-[YYYY-MM-DD].md`
- `4-Knowledge/log.md` has a `lint` entry with the counts
- The suggestions are ranked
- A clean report came with the caveat about what this check cannot see

## Hard constraints

- Lint reports, it does not repair. Pages change after the human agrees, never during the check.
- Sources in `5-Raw/` are read-only. A contradiction between a page and its source is a finding about the page.
