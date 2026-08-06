---
name: process-inbox
description: Process new files from 2-Inbox/ and Clippings/ through the Karpathy knowledge loop - enrich, compile to 4-Knowledge/ wiki, archive to 5-Raw/
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

### 2. Check for duplicates

Search `4-Knowledge/` and `5-Raw/` - has this topic already been processed?
- If yes -> UPDATE the existing wiki page (add new insights, add the source to the YAML)
- If no -> CREATE a new wiki page

### 3. Compile into Knowledge

Create or update a wiki page in `4-Knowledge/`:

```markdown
---
title: [Readable Title]
created: [YYYY-MM-DD]
sources:
  - source-file-1.md
  - source-file-2.md
---

# [Readable Title]

[Compiled content - synthesis, not copy-paste]

[Every claim cites its source: [source: file-name.md]]

## Related
- [[Another Wiki Page]]
```

**Rules:**
- Readable file name: `Discovery Methods.md`, not `discovery-methods.md`
- One page per concept, not one page per source
- Put it in the right `4-Knowledge/` subfolder (create one if nothing fits, minimum three pages per subfolder)
- Add `[[backlinks]]` to related pages
- Cite the source: `[source: file-name.md]`

### 4. Archive the source

Move the processed file from `2-Inbox/` or `Clippings/` to `5-Raw/`.

### 5. Update the index and log

- Add or update the page's entry in `4-Knowledge/index.md`
- Append an entry to `4-Knowledge/log.md`

### 6. Report

```
Processed: "file-name.md"
  -> Wiki: 4-Knowledge/[Subfolder]/[Page Title].md (created/updated)
  -> Archive: 5-Raw/
```

## Batch mode (--all)

1. List the files in `2-Inbox/` and `Clippings/`
2. For each: analyse, compile, archive
3. Show a summary:

| File | Wiki | Status |
|------|------|--------|
| article.md | 4-Knowledge/AI/Title.md | created |
| thread.md | 4-Knowledge/Product/Title.md | updated |

4. Report: X processed, Y skipped, Z flagged

## STOP - red flags

- Modifying a file in `5-Raw/` (the archive is immutable)
- Creating a wiki page with a slug name instead of a readable title
- Copying content 1:1 instead of compiling it
- Moving a file without creating or updating a wiki page
- Finishing without updating `index.md` and `log.md`
