---
name: query
description: Answers from the compiled wiki in 4-Knowledge/, with citations and a saved output file. Use when the human asks something this vault should already know, wants a briefing or comparison built from ingested sources, or asks what the vault is missing on a topic.
---

# Query

Answer from the wiki, not from memory, and keep the answer so the next question starts further along.

Write the answer and every file you produce in the language the human is using.

## How to invoke

- Any question the vault plausibly covers
- "What do we know about X?"
- "Compare X and Y from what I have"
- "Write me a briefing on X"
- `/query`

## How it works

### 1. Find the pages

Read `4-Knowledge/index.md` first. It is the map, and it exists so you do not have to read every page to find three.

Pick the pages that bear on the question, entity pages included when the question names a person, company or tool.

If the index promises a page that is not on disk, or you find a page the index never lists, tell the human. Both are real findings.

### 2. Read them

Read the pages you picked, in full. Follow `[[links]]` one hop out when the question sits between two topics.

### 3. Answer

Cite every claim with `[source: page-name.md]`, naming the wiki page you actually read.

Where the wiki disagrees with itself, show both sides and name the sources. A `> CONTRADICTION:` marker is a finding to surface, not noise to smooth over.

Where the wiki is thin, say so in the answer. If you add something from outside the vault, mark it plainly as outside knowledge so the human can tell the two apart.

### 4. Save the output

Write `9-Outputs/[YYYY-MM-DD]-[short-slug].md`:

```markdown
---
question: [the question, as asked]
date: [YYYY-MM-DD]
pages: [wiki pages used]
filed_back: [page name, or: no]
---

# [Question as a title]

[The answer, with [source: page-name.md] citations]

## What this is built on
- [[Page A]] - what it contributed
- [[Page B]] - what it contributed

## Gaps
[What the wiki could not answer. The most useful section in the file: it tells
the human what to read next.]
```

A one-line lookup does not need a file. Say out loud that you skipped it, so the human knows this answer was not kept.

When the answer has a shape that prose flattens - a comparison across dimensions, a timeline, a distribution - offer the better format and save it beside the markdown under the same slug. The format rules are in `8-System/brain.md` under Conventions.

### 5. Log it

Append a `query` entry to `4-Knowledge/log.md`. That file carries the format.

### 6. Offer to file it back

If the answer holds synthesis that is on no page yet - a comparison, a connection, a conclusion the human will want again - offer to write it into `4-Knowledge/` as a new page or a section on an existing one, then update `4-Knowledge/index.md` and log it as an `update`.

This is the step that makes asking questions improve the wiki instead of only spending it. It is also the human's call: ask, and wait.

## Self-check

- Every claim carries a `[source: ...]` citation
- The output file exists, or you said out loud that you skipped it
- `4-Knowledge/log.md` has a `query` entry pointing at that file
- `## Gaps` names something real rather than being left empty because it was easier
- Anything you contributed from outside the vault is marked as such

## Hard constraints

- The markdown output is canonical. An HTML page or a deck is a view of it, never a replacement.
- Synthesis goes back into `4-Knowledge/` only after the human agrees.
- Sources in `5-Raw/` are read-only. Cite them and leave them as they are.
