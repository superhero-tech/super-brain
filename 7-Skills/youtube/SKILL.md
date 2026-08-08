---
name: youtube
description: Captures a YouTube video as a source note and a wiki page. Use when the human drops a video URL, wants a talk or tutorial turned into notes, or asks what a specific video said about a topic.
---

# YouTube Video Summary

Turns a YouTube video into a structured note, then compiles that note into a wiki page in Knowledge.

## When to use

- You want a video turned into a clean note with metadata and key ideas
- For tutorials the output is a step-by-step guide, not a summary

## Requirements

This skill pulls metadata and subtitles with `yt-dlp`. Install it once:

```bash
brew install yt-dlp     # macOS
pip install yt-dlp      # everywhere else
```

Without `yt-dlp` the skill still works, just slower: take the video ID from the URL and search the web for the metadata, then ask the human to paste the transcript from YouTube's transcript panel. Say which route you are taking so they know why it takes longer.

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

### 5. Save the note and hand it to the ingest

Save the note to `2-Inbox/`, then run the `ingest` skill on it. That skill owns everything downstream: mapping the video against the wiki, writing the pages, linking them, updating the index and log, and archiving the note to `5-Raw/`.

Tell the ingest one thing it cannot see on its own: **talks are entity-heavy.** The speaker, their company and every tool they name by name are entity candidates, and a good talk moves more pages than an article of the same length.

This skill's job ends at a note good enough to compile.

## Self-check

- Could someone hold a conversation about this topic reading only my note?
- For tutorials: could someone RUN the workflow without watching the video?
- Did I capture the concrete numbers and metrics?
- Did I catch the Q&A section?
- Did I avoid AI filler words (delve, tapestry, pivotal, foster)?
- Is the note in `2-Inbox/` and handed to the ingest, rather than left sitting there?

## Cleanup

```bash
rm -f /tmp/yt_transcript*
```
