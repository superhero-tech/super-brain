---
name: youtube
description: Create a video summary note from a YouTube URL, then compile into 4-Knowledge/ wiki page via Karpathy method
---

# YouTube Video Summary

Turns a YouTube video into a structured note, then compiles that note into a wiki page in Knowledge.

## When to use

- You want a video turned into a clean note with metadata and key ideas
- For tutorials the output is a step-by-step guide, not a summary

## How to invoke

- `/youtube https://youtube.com/watch?v=...`
- "Make a note from this video: [URL]"

## How it works

### 1. Pull the metadata

```bash
yt-dlp --skip-download --print "%(title)s|||%(channel)s|||%(upload_date)s|||%(description).500s" "$ARGUMENTS"
```

If yt-dlp fails: extract the video ID from the URL and use web search.

### 2. Get the transcript

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs "en" --sub-format "vtt" -o "/tmp/yt_transcript" "$ARGUMENTS"
```

Add more languages to `--sub-langs` when you need them. If it fails, ask the user to paste the transcript from YouTube.

### 3. Classify the video

- **Tutorial/Explainer**: walkthrough, demo, how-to -> output a step-by-step guide
- **Idea/Opinion**: thesis, interview, perspective -> output key ideas plus quotes

### 4. Generate the note

**YAML frontmatter:**
```yaml
---
date: YYYY-MM-DD
title: "Video Title"
author: Channel Name
source: [YouTube URL]
topics:
  - topic-1
  - topic-2
source_type: video
---
```

This is the frontmatter of the **source note** that lands in `2-Inbox/` and later `5-Raw/`. It is not wiki-page frontmatter - wiki pages use `type: concept | entity`. Do not copy this block onto the wiki page.

**For tutorials:**
```markdown
# Title

## What this covers
[1-2 sentences]

## Step-by-Step
### Step 1: [Action]
[What to click, type, configure. Imperative.]

## Tips & Gotchas
- Practical notes and limitations

## Source
[URL]
```

**For ideas/opinions:**
```markdown
# Title

## Key Ideas
- (5-10 key ideas - be specific)

## Summary
[3-5 paragraphs]

## Notable Quotes
> "Quote from the video"

## Source
[URL]
```

**What to extract:**
- Concrete examples and anecdotes (do not abstract them away)
- Numbers and metrics
- "here is what we actually do" moments - where speakers reveal practice instead of theory
- Contrarian claims
- Tools and products by name
- Metaphors and mental models
- Q&A sections - the best nuggets hide there

### 5. Save and process (Karpathy loop)

**Step A:** Save the note to `2-Inbox/`

**Step B:** Map the video against `4-Knowledge/index.md`. List everything it touches, marked by kind (concept or entity) and by state (primary / existing / new). Videos are entity-heavy - the speaker, their company, and every tool they name are candidates. An entity earns a page at two or more sources, or if it is central to this one.

**Step C:** Write the primary page in the right `4-Knowledge/` subfolder - readable file name, `[source: ...]` citations, and this frontmatter:

```yaml
---
title: [Readable Title]
type: concept
created: [YYYY-MM-DD]
last_updated: [YYYY-MM-DD]
source_count: [n]
status: draft
sources:
  - note-file.md
---
```

**Step D:** Update every existing page the video touches, and write the entity pages that earned one (`type: entity`, `entity_kind`, short, links out to where the reasoning lives). Add what the video adds, cite it, link both ways. A 40-minute talk usually moves several pages. Updating one and stopping defeats the point.

**Step E:** Move the note from `2-Inbox/` to `5-Raw/`

**Step F:** Update `4-Knowledge/index.md` and append an `ingest` entry to `4-Knowledge/log.md`, listing every page you touched

## Self-check

- Could someone hold a conversation about this topic reading only my notes?
- For tutorials: could someone RUN the workflow without watching the video?
- Did I capture the concrete numbers and metrics?
- Did I catch the Q&A section?
- Did I avoid AI filler words (delve, tapestry, pivotal, foster)?
- Did I update the other pages this video touches, or just write one and stop?

## Cleanup

```bash
rm -f /tmp/yt_transcript*
```
