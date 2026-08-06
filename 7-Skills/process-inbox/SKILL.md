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

Read `4-Knowledge/index.md`. Then list **everything** this source touches - every concept, method, tool, company, person and claim in it - and mark each one as:

- **primary** - the source's main concept, gets the new or heavily updated page
- **existing** - already has a page, needs an update from this source
- **new** - worth a page of its own later, no page yet

This list is the actual work. Steps 3 and 4 just execute it.

### 3. Write the primary page

Create or update the page for the primary concept:

```markdown
---
title: [Readable Title]
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

### 5. Archive the source

Move the processed file from `2-Inbox/` or `Clippings/` to `5-Raw/`.

### 6. Update the index and log

- Add or update every touched page's entry in `4-Knowledge/index.md`
- Append an `ingest` entry to `4-Knowledge/log.md` listing **every** page you touched, not just the primary one

### 7. Report

```
Processed: "file-name.md"
  -> Primary: 4-Knowledge/[Subfolder]/[Page Title].md (created)
  -> Updated: [Page B], [Page C], [Page D]
  -> New pages worth writing: [concept X], [concept Y]
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
- Moving a file without creating or updating a wiki page
- Finishing without updating `index.md` and `log.md`
