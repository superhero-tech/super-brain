![Wojtek Strzałkowski and Piotr Kacała, AI Product Heroes](assets/cover.png)

# A Second Brain for Product Builders

A vault your AI reads, writes and maintains. From the team behind [AI Product Heroes](https://aiproductheroes.pl).

Every chat starts from zero. You paste the same context, get a good answer, close the tab, and the thinking is gone. Next week you ask a related question and do it all again. The tool got smarter; your setup did not.

Super Brain is a folder instead of a conversation. Sources compile into a linked wiki. Questions get answered from that wiki and saved, so asking makes it better instead of just using it up. Projects carry enough context that an agent can join one cold. Your profile lives in a file, not a system prompt, so it moves with you between tools and jobs.

It is an adaptation of [Andrej Karpathy's LLM knowledge base method](https://x.com/karpathy/status/2039805659525644595), with the parts a working product builder actually needs bolted on.

## Setup

```
git clone https://github.com/superhero-tech/super-brain
cd super-brain
claude
```

Then run `/second-brain-setup` and answer the questions. That is the whole install.

Obsidian is the recommended window onto it (`Open folder as vault`), but nothing depends on it. [SETUP.md](SETUP.md) covers the other routes: Claude Cowork for non-developers, OpenCode with a ChatGPT subscription or a free model, and any AI-enabled IDE.

## Why this exists

We have been running this method on our own work since April and teaching it to people who then go and break it in interesting ways. The same four failures keep showing up.

**Notes accumulate, knowledge does not.** Most systems file a summary per source and call it a knowledge base. `ingest` maps everything a source touches, writes one page per concept, and updates every other page that source has something to say about, with links in both directions. One article moves five pages or it tells you why it did not.

**Good answers evaporate into the terminal.** You ask a sharp question, get a synthesis nobody has written down before, and lose it when the tab closes. `query` saves every substantial answer with its citations and a section naming what the wiki could not answer, then offers to file the new thinking back in.

**Wikis rot quietly.** A subtly wrong page gets built on until five pages agree on the same error. `lint` runs monthly, sorts findings into errors, warnings and notes, and ranks what to fix first. It reports; you decide.

**Projects you cannot pick up cold.** A brief tells you what a project was supposed to be. `project-update` keeps the log that tells you what it became, and refreshes the index so the next session starts from the truth.

## The skills

Five workflows, one skill each, plus setup, video capture and a way to find out whether you actually understand what you have collected. They trigger on their own when the conversation calls for them - say "process what I dropped in the inbox" and `ingest` shows up - or you invoke them directly with `/query`. Claude reads them from `.claude/skills/`, Codex and ChatGPT from `.agents/skills/`; both are published from `7-Skills/`, so they work on a fresh clone without setup.

| Skill | What it does |
|---|---|
| **`ingest`** | Turns a source in `2-Inbox/` into wiki. Lists everything the source touches and checks that reading with you before writing, then updates every page it touches with links in both directions. A substantial source moves five pages, or it says why it did not. |
| **`query`** | Answers from the wiki with `[source: ...]` citations, saves the answer to `9-Outputs/` with a section naming what the wiki could not answer, and offers to file new synthesis back as a page. |
| **`lint`** | Monthly health check. Ten checks sorted into errors, warnings and notes: contradictions, uncited claims, orphans, stale frontmatter, people who became hubs without a page. Writes a ranked report and stops, because repair is a separate decision. |
| **`project-start`** | Opens a project through an interview that pushes back once per section. "Everyone" is not a segment and "more engagement" is not an outcome. "I do not know" is a valid answer that becomes an open question. |
| **`project-update`** | Turns what happened into an artefact, a log entry and a fresh index row. The last two decay first because they produce nothing visible, and a stale index means the next session starts from a false picture. |
| **`second-brain-setup`** | Writes your profile into `8-System/about.md`, from a pasted assessment (Gallup, DISC, MBTI) or a short interview. Re-run it after a role change and it updates only what moved. |
| **`youtube`** | Turns a video into a source note with metadata, key ideas and quotes, then hands it to `ingest`. Wants `yt-dlp`; without it, it asks you to paste the transcript and carries on. |
| **`feynman`** | Explains a page in words a twelve-year-old owns, then names every place the explanation went thin, sorted into the wiki's fault, the sources' fault and its own. Saves the session to `9-Outputs/` so you can see what you have been studying. Edits no wiki page. |

The one to try first: drop three articles on one topic into `2-Inbox/`, run `ingest` on each, then ask `query` something none of them answers on its own.

## What we bolted on

Karpathy's document is a pattern, not a build. Three layers, three operations, an index and a log - deliberately abstract, ending with a note that tells you to hand it to your agent and work the specifics out together. That is the right way to publish an idea and the wrong way to start on a Tuesday morning.

Super Brain is one instantiation of it with the decisions already made. Same three layers, same ingest/query/lint loop, same index-first navigation and no embeddings. What sits on top:

| What we added | Why |
|---|---|
| **Operations as skills, not sections of a schema** | Each workflow is a `SKILL.md` with its own self-check and hard constraints, loaded only when it fires. Published to `.claude/skills/` and `.agents/skills/`, so the same vault runs on Claude and on Codex. |
| **A project layer** | `3-Projects/`, one folder per project, with a brief, rules and an append-only log. Karpathy's wiki is a reading artefact. This one also has to hold work in progress, so an agent can join a project cold. The brief is what the project was supposed to be; the log is what it became. |
| **A profile in a file** | `8-System/about.md` holds who you are and how you want to be worked with. It moves between tools and jobs. A system prompt does not. |
| **A check-in before anything gets written** | `ingest` shows you its reading of a source and waits. A wrong page written today is a wrong answer in every query for a month, and nobody notices until it has been built on. This is the cheapest place to catch it. |
| **Frontmatter that `lint` can sort on** | `status`, `source_count` and `last_updated` on every page, plus ten checks split into errors, warnings and notes, ranked by what they unblock. A page with no `last_updated` is invisible to the health check, and an unranked report gets read once. |
| **Gaps as a required section** | Every saved answer names what the wiki could not answer. That section is what tells you which source to go and find next, and it is the one most likely to be left empty because it was easier. |
| **`feynman`** | Explains a page in plain words and sorts what went thin into the wiki's fault, the sources' fault and its own. The failure this pattern invites and does not address is you losing the thread of a wiki that something else read for you. |
| **A limits file the agent has to read** | `8-System/limits.md` names five ways this breaks, and `8-System/brain.md` makes the agent read it before it tells you the wiki is sure about something. |

What we left out: Karpathy suggests reaching for a real search tool - [qmd](https://github.com/tobi/qmd) or something like it - once the index stops being a sufficient map. We stayed index-only and declared the ceiling instead: roughly a hundred pages, one vault per domain, both written down in [limits.md](8-System/limits.md). Naming a limit is not removing it. If your vault outgrows the index, that is the first thing to go and fix, and the original pattern already tells you how.

## What it does badly

Read [8-System/limits.md](8-System/limits.md) before you trust it on anything expensive. Error compounding is real, a wiki that looks authoritative gets checked less than it should, and the index-first approach has a ceiling around a hundred pages. We would rather you knew that from us.

## Who's behind this

We're Wojtek and Piotr, founders of [Superhero.tech](https://superhero.tech) and [AI Product Heroes](https://aiproductheroes.pl), a course where product people learn to build real products in the AI era. This is the vault we use on our own work, not a demo.

If this is your kind of thing, the [newsletter](https://newsletter.superhero.tech) is where we publish the rest.
