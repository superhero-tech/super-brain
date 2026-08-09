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

We have run this method on our own work for a year and taught it to people who then went and broke it in interesting ways. The same four failures keep showing up.

**Notes accumulate, knowledge does not.** Most systems file a summary per source and call it a knowledge base. `ingest` maps everything a source touches, writes one page per concept, and updates every other page that source has something to say about, with links in both directions. One article moves five pages or it tells you why it did not.

**Good answers evaporate into the terminal.** You ask a sharp question, get a synthesis nobody has written down before, and lose it when the tab closes. `query` saves every substantial answer with its citations and a section naming what the wiki could not answer, then offers to file the new thinking back in.

**Wikis rot quietly.** A subtly wrong page gets built on until five pages agree on the same error. `lint` runs monthly, sorts findings into errors, warnings and notes, and ranks what to fix first. It reports; you decide.

**Projects you cannot pick up cold.** A brief tells you what a project was supposed to be. `project-update` keeps the log that tells you what it became, and refreshes the index so the next session starts from the truth.

## The skills

Five workflows, one skill each, plus setup and video capture. They trigger on their own when the conversation calls for them - say "process what I dropped in the inbox" and `ingest` shows up - or you invoke them directly with `/query`.

**`ingest`** turns a source in `2-Inbox/` into wiki. It lists everything the source touches before writing anything and checks that reading with you, then writes the primary page and updates every other page the source has something to say about, with links in both directions. A substantial source moves five pages, or it tells you why it did not.

**`query`** answers from the wiki with `[source: ...]` citations, then saves the answer to `9-Outputs/` with a section naming what the wiki could not answer. When the answer contains synthesis nobody has written down yet, it offers to file that back as a page. Questions make the wiki better instead of only spending it.

**`lint`** is the monthly health check. Ten checks sorted into errors, warnings and notes: pages that contradict each other, claims with no citation, orphans, stale frontmatter, people who became hubs without a page of their own. It writes a ranked report and stops. Repair is a separate decision, and it says so.

**`project-start`** opens a project through an interview that pushes back once per section. "Everyone" is not a segment, "more engagement" is not an outcome, and an empty list of open questions on day one means the project has not been thought about yet. "I do not know" is a valid answer that becomes an open question.

**`project-update`** turns what happened into an artefact in the right subfolder, an entry in the project log and a fresh row in the index. Those last two are the steps that decay, because they produce nothing visible - and a stale index means the next session starts from a false picture of what is live.

**`second-brain-setup`** writes your profile into `8-System/about.md`, either from a pasted assessment (Gallup, DISC, MBTI, whatever you have) or a short interview. Run it again when your role changes and it updates only what moved.

**`youtube`** turns a video into a source note with metadata, key ideas and quotes, then hands it to `ingest`. It wants `yt-dlp` installed; without it, it asks you to paste the transcript and carries on.

The one to try first: drop three articles on one topic into `2-Inbox/`, run `ingest` on each, then ask `query` something none of them answers on its own.

**Zero setup:** no API keys, no accounts, no database. Markdown files and folders. `youtube` wants `yt-dlp` installed and degrades gracefully without it.

## What it does badly

Read [8-System/limits.md](8-System/limits.md) before you trust it on anything expensive. Error compounding is real, a wiki that looks authoritative gets checked less than it should, and the index-first approach has a ceiling around a hundred pages. We would rather you knew that from us.

## Who's behind this

We're Wojtek and Piotr, founders of [Superhero.tech](https://superhero.tech) and [AI Product Heroes](https://aiproductheroes.pl), a course where product people learn to build real products in the AI era. This is the vault we use on our own work, not a demo.

If this is your kind of thing, the [newsletter](https://readwojtech.substack.com) is where we publish the rest.
