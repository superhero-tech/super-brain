---
name: ingest
description: Compiles a source from 2-Inbox/ into the wiki, across every page it touches, then archives it. Use when the human drops something in the inbox, says to process it, or wants a backlog of clippings worked through.
---

# Ingest

Turn a source into wiki. Not one summary page per file - one page per concept, plus every existing page this source has something to say about.

Write wiki pages in the language the human writes in. One language per page.

## How to invoke

- "Process this", "run an ingest", "I dropped something in Inbox"
- "Process the whole inbox" for batch mode
- `/ingest`

Sources live in `2-Inbox/`. If the human clips with Obsidian Web Clipper on its default settings, check `Clippings/` too.

## How it works

### 1. Read the source

End to end, before forming a view of it. Note what it is - article, thread, tutorial, transcript, note - and who wrote it.

### 2. Map it against the wiki

Read `4-Knowledge/index.md`. Then list everything the source touches and mark each item twice.

By kind:
- **concept** - an idea, framework, method or pattern
- **entity** - a person, company, tool or product

By state:
- **primary** - the source's main concept, gets the new or heavily updated page
- **existing** - has a page already, needs an update from this source
- **new** - worth its own page, does not have one yet

An entity earns a page when it appears in two or more sources, or is central to this one. A name mentioned once in passing gets a citation, not a page.

Also check `5-Raw/` - if this source has been processed before, you are updating pages, not creating them.

This list is the actual work. Everything after it is execution.

### 3. Check in before writing

Show the human what you found, in three or four lines: what the source argues, which pages you are about to touch, and anything in it that contradicts what the wiki already says. Then wait.

A wrong page written now is a wrong answer in every query for the next month, and nobody will notice until it has been built on. This is the cheapest place to catch it. Batch mode is the only exemption.

### 4. Write the pages

Load `references/page-templates.md` now - it has the frontmatter and the shape for both concept and entity pages.

Write the primary page first, then every page marked **existing**. For each of those: add what this source adds, cite it, and link to the primary page.

**Link in both directions.** A `[[link]]` from the new page to an old one is half a link. Add the return link on the old page. One-directional links are how pages become orphans.

A substantial source moves five or more pages. Touching one page and stopping turns the wiki into a pile of summaries. If a source genuinely touched one page, say so and say why - early on the honest answer is usually that the wiki is still too small.

Two rules hold on every page you touch:

- Cite the source on every claim: `[source: file-name.md]`
- Flag contradictions instead of overwriting: `> CONTRADICTION: [old claim] vs [new claim] from [source]`

### 5. Update the index and log

- `4-Knowledge/index.md`: add the new pages, refresh the descriptions of changed ones. Concepts and entities are listed separately.
- `4-Knowledge/log.md`: append an `ingest` entry listing **every** page you touched, not only the primary one. That file carries the format.

### 6. Archive the source

Move the file from `2-Inbox/` or `Clippings/` to `5-Raw/`, and any images that came with it to `5-Raw/assets/`. Never rename an asset afterwards - the pages referencing it will not follow.

### 7. Report

```
Processed: "file-name.md"
  -> Primary: 4-Knowledge/[Subfolder]/[Page Title].md (created)
  -> Updated: [Page B], [Page C], [Page D]
  -> Entities: [Name] (created), [Name] (updated)
  -> Worth writing later: [concept X], [entity Y]
  -> Archive: 5-Raw/
```

## Batch mode

For a backlog, work through the files one at a time and skip the step 3 check-in. Say up front that batch mode runs unsupervised and produces thinner pages than one-at-a-time ingest, because nobody is correcting the reading.

Finish with a table of file, primary page, how many other pages moved, and the created/updated status, then the totals.

## Daily notes

`1-Daily/` is a source too, but never ingest it unasked - daily notes are personal, unfinished, and full of things that were true for one afternoon.

When the human asks you to go through a week or a month of them, read the range and sort what you find: anything general goes to Knowledge as an ingest, anything about a specific project goes to that project's log as an update.

## Self-check

- Every page you listed as **existing** was actually opened and updated
- Every new link has its return link
- `4-Knowledge/index.md` lists the new pages, `log.md` lists all of them
- The source is in `5-Raw/` and its images are in `5-Raw/assets/`
- If only one page moved, you said why

## Hard constraints

- Files in `5-Raw/` are read-only once archived. Cite them, leave them alone.
- Contradictions get flagged, never silently resolved.
- A source moves out of the inbox only after its pages exist.
- Entity pages stay short and link out. The reasoning lives on the concept page.
