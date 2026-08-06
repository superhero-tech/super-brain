---
name: process-inbox
description: Process new files from 2-Inbox/ and Clippings/ through the Karpathy knowledge loop - compile into the 4-Knowledge/ wiki across every page the source touches, then archive to 5-Raw/
---

# Process Inbox

Runs new files from `2-Inbox/` and `Clippings/` through the Karpathy knowledge loop.

## When to use

- You dropped new files into Inbox or Clippings (articles, transcripts, notes, web clippings)
- You want to process everything new in one command

## How to invoke

- "Process the inbox"
- "Run an ingest"
- "What is new in the inbox?"
- `/process-inbox`
- `/process-inbox file-name.md`
- `/process-inbox --all`

## How it works

For every file in `2-Inbox/` or `Clippings/`:

### 1. Read and analyse

Read the full file. Pull out:
- The topic and key concepts
- The author/source
- The type: article, thread, tutorial, video, note?

### 2. Map it against the wiki

Read `4-Knowledge/index.md`. Then list **everything** this source touches and mark each item twice.

By kind:
- **concept** - an idea, framework, method or pattern
- **entity** - a person, company, tool or product

By state:
- **primary** - the source's main concept, gets the new or heavily updated page
- **existing** - already has a page, needs an update from this source
- **new** - worth a page of its own, no page yet

An entity earns a page when it appears in two or more sources, or is central to this one. A name mentioned once in passing gets a citation, not a page.

This list is the actual work. Steps 3 and 4 just execute it.

### 2b. Check in before writing

Show the human what you found, in three or four lines: what the source argues, which pages you are about to touch, and anything that contradicts what the wiki already says. Then wait.

Skip this only in batch mode. A wrong page written now is a wrong answer in every query for the next month - this is the cheapest place to catch it.

### 3. Write the primary page

Create or update the page for the primary concept:

```markdown
---
title: [Readable Title]
type: concept
created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
source_count: [how many sources this page is built on]
status: draft
sources:
  - source-file-1.md
  - source-file-2.md
---

# [Readable Title]

[Compiled content - synthesis, not copy-paste]

[Every claim cites its source: [source: file-name.md]]

## Related
- [[Another Wiki Page]] - how it connects
```

**Rules:**
- Readable file name: `Discovery Methods.md`, not `discovery-methods.md`
- One page per concept, not one page per source
- Put it in the right `4-Knowledge/` subfolder (create one if nothing fits, minimum three pages per subfolder)
- Bump `last_updated` and `source_count` on every edit. Set `status: needs_update` if the new source contradicts what is already there.

### 4. Update every other page the source touches

For each page marked **existing** in step 2:

- Add what this source adds to it, with a `[source: ...]` citation
- Add a `[[link]]` to the primary page - and make sure the primary page links back
- Bump `last_updated` and `source_count`
- Flag contradictions instead of overwriting: `> CONTRADICTION: [old] vs [new] from [source]`

A substantial source moves five or more pages. **Touching one page and stopping is the failure mode of this skill** - it turns the wiki into a pile of summaries. If a source really did touch only one page, say so and say why.

### 4b. Write or update the entity pages

For every person, company, tool or product marked **entity** in step 2 that earns a page:

```markdown
---
title: [Entity Name]
type: entity
entity_kind: person | company | tool | product
created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
source_count: [n]
status: draft
sources:
  - source-file.md
---

# [Entity Name]

[One paragraph. What this is and why it earns a page here.]

## What they argue / What it does
- [One line per claim or capability, each cited]

## Where it shows up
- [[Concept Page]] - what this entity contributed there

## Open questions
```

**Keep entity pages short.** The reasoning belongs on the concept page; the entity page says who said what and links to it. An entity page longer than the concept pages it points at means the argument landed in the wrong file.

### 5. Archive the source

Move the processed file from `2-Inbox/` or `Clippings/` to `5-Raw/`, and any images that came with it to `5-Raw/assets/`. Never rename an asset after this - the pages referencing it will not follow.

### 6. Update the index and log

- Add or update every touched page's entry in `4-Knowledge/index.md`
- Append an `ingest` entry to `4-Knowledge/log.md` listing **every** page you touched, not just the primary one

### 7. Report

```
Processed: "file-name.md"
  -> Primary: 4-Knowledge/[Subfolder]/[Page Title].md (created)
  -> Updated: [Page B], [Page C], [Page D]
  -> Entities: [Name] (created), [Name] (updated)
  -> Worth writing later: [concept X], [entity Y]
  -> Archive: 5-Raw/
```

## Batch mode (--all)

Batch mode runs unsupervised. Say so before you start - single-source ingest with the human in the loop produces better pages, and it is the default in the method for a reason.

1. List the files in `2-Inbox/` and `Clippings/`
2. For each: map, compile, cross-update, archive
3. Show a summary:

| File | Primary page | Also updated | Status |
|------|------|------|--------|
| article.md | 4-Knowledge/AI/Title.md | 4 pages | created |
| thread.md | 4-Knowledge/Product/Title.md | 2 pages | updated |

4. Report: X processed, Y skipped, Z flagged

## STOP - red flags

- Modifying a file in `5-Raw/` (the archive is immutable)
- Creating a wiki page with a slug name instead of a readable title
- Copying content 1:1 instead of compiling it
- Writing the primary page and skipping step 4
- Adding a `[[link]]` in one direction only
- Creating an entity page for every name in the source, including the ones mentioned once
- Writing the argument onto the entity page instead of the concept page it belongs to
- Compiling without the check-in in step 2b, outside batch mode
- Moving a file without creating or updating a wiki page
- Finishing without updating `index.md` and `log.md`
