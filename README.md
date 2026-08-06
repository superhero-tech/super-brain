# Super Brain

A second brain for product builders: a folder of markdown files that an AI reads, writes and maintains for you.

Raw sources go in, a linked wiki comes out, and every question you ask is answered from that wiki instead of from scratch. Answers get saved and filed back, so asking questions makes the wiki better rather than just spending it. Projects live alongside the wiki with their own briefs, rules and logs. The AI knows you from a profile file, not a system prompt - so it moves with you between tools.

**Start here: [SETUP.md](SETUP.md)**

## Layout

| Folder | What lives here |
|---|---|
| `1-Daily/` | Daily notes |
| `2-Inbox/` | New material waiting to be processed |
| `3-Projects/` | Active projects, one folder each. See [3-Projects/README.md](3-Projects/README.md) |
| `4-Knowledge/` | The compiled wiki. The AI owns this. |
| `5-Raw/` | The source corpus, plus `assets/` for their images. Immutable. |
| `6-Templates/` | Document templates |
| `7-Skills/` | Runnable agent skills, linked into `.claude/skills/` so they work as slash commands |
| `8-System/` | Agent instructions, your personal profile, and [where this method breaks](8-System/limits.md) |
| `9-Outputs/` | Answers and reports the AI produces. Every substantial question lands here. |

`CLAUDE.md` and `AGENTS.md` are the entry points agents read first. They point at `8-System/brain.md`, which holds the actual operating instructions.

## Requirements

Any AI tool that can read and write local files - Claude Code, Claude Cowork, OpenCode, Cursor, Windsurf, Codex. Obsidian is recommended as the viewer but not required.

## Before you trust it

Read [8-System/limits.md](8-System/limits.md). The method works, and it fails in five specific ways - error compounding being the one that will actually bite you.

## Credits

See [CREDITS.md](CREDITS.md).
