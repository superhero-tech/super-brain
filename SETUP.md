# Setting up your Super Brain

---

## What this is and why you want it

Super Brain is not a chat. It is a folder on your disk - a set of files that an AI reads, writes and maintains. Your knowledge compiles into a wiki, your projects get their own place, and the AI knows you from a profile file instead of a system prompt.

The point is portability. A chat forgets you when the conversation ends and it is locked to one tool. A folder is not. You take it to the next project, the next tool, the next job.

### The Karpathy method

The knowledge loop is an adaptation of Andrej Karpathy's LLM knowledge base method:

1. You dump raw material into a folder (articles, transcripts, notes)
2. You tell the AI: "process this"
3. The AI reads the source and compiles it into a wiki page - not one summary per file, but one page per concept, with links between concepts and citations back to sources
4. After 20-30 sources you have a knowledge base that answers questions faster and better than searching through the original files

Super Brain adds four things on top: projects, document templates, agent skills and a personal profile - so the AI knows not only WHAT you know, but HOW to work with you.

### Chat vs Super Brain

| | AI chat | Super Brain |
|---|---|---|
| Where it lives | System prompt inside one tool | A folder on your disk |
| Portability | Locked to one tool | Works with any AI |
| Knowledge | Dies with the conversation | Compiles into a wiki, grows with every source |
| Personalisation | System prompt | `about.md` - editable, portable |
| Projects | No structure | Separate folders with briefs, decisions, prototypes |
| When you move on | You keep a prompt | You keep the whole folder |

---

## Before you start

### 1. Get the folder onto your disk

Clone it, or unzip it anywhere - `Documents`, `Desktop`, Dropbox, OneDrive. The location does not matter as long as the folder does not disappear.

### 2. Install Obsidian (recommended)

Obsidian is a free markdown editor - your window into the Super Brain. The AI writes the files, Obsidian shows them live with backlinks and a graph.

1. Go to https://obsidian.md
2. Download (macOS / Windows / Linux - free)
3. Install and launch
4. Choose **"Open folder as vault"** and point it at your Super Brain folder

### 3. Install the Obsidian Web Clipper (optional)

A browser extension that saves web pages as markdown straight into your Super Brain.

1. https://obsidian.md/clipper (or search "Obsidian Web Clipper" in the Chrome/Firefox store)
2. Install it
3. In the Web Clipper settings, set the default save folder to `2-Inbox`

From then on, articles land in your Inbox in one click.

---

## Pick your path

| Path | For whom | Cost |
|---|---|---|
| **A. Claude Code / Cowork** | You have a Claude Pro or Max subscription | ~$20/mo |
| **B. OpenCode + ChatGPT** | You have ChatGPT Plus/Pro and do not use Claude | ~$20/mo |
| **C. OpenCode + a free model** | You do not want to pay for AI at all | Free |
| **D. Cursor / Windsurf / Antigravity** | You already have an AI-enabled IDE | Depends on the IDE |

Every path works on the SAME folder. Change your mind later and you switch tools, not files.

---

## Path A: Claude Code / Cowork

The best option if you have Claude Pro. Two versions:

### A1: Claude Cowork (for non-developers)

Cowork is a tab in Claude Desktop with full file access.

1. Open **Claude Desktop** (download from https://claude.ai/download if you do not have it)
2. Click the **Cowork** tab (next to Chat)
3. Point it at the Super Brain folder as the working directory
4. **Test:** type into the chat:

```
Read CLAUDE.md and tell me what you see.
```

If the AI comes back talking about `brain.md` and `about.md`, it works.

5. **Run the setup skill:** type `/second-brain-setup` (if the skill is installed) or:

```
Read 7-Skills/second-brain-setup/SKILL.md and run the workflow described in that file.
```

### A2: Claude Code (for developers)

Claude Code is a CLI with full filesystem access.

1. Install Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
```

2. Go to the Super Brain folder and launch it:

```bash
cd /path/to/your/super-brain
claude
```

3. **Test:**

```
Read CLAUDE.md and tell me what you see.
```

4. **Run the setup skill:**

```
Run the second-brain-setup skill
```

---

## Path B: OpenCode + ChatGPT

### What is OpenCode?

OpenCode is a free, open-source tool for working with AI on local files - similar to Claude Code, but it supports many providers (OpenAI, Google, open-source models and others). If you do not have Claude Pro but you do have ChatGPT Plus/Pro, OpenCode lets you use OpenAI models on your Super Brain within your existing subscription. No API key needed.

### Install

Go to https://opencode.ai/download and get the app for your system (macOS / Windows / Linux).

For developers, via terminal instead:

```bash
npm i -g opencode-ai
```

### Connect ChatGPT

1. Go to the Super Brain folder and launch it:

```bash
cd /path/to/your/super-brain
opencode
```

2. Type `/connect`
3. Pick **OpenAI** from the provider list
4. Pick **"ChatGPT Plus/Pro"** as the auth method
5. A browser opens - log in with your ChatGPT account
6. The token comes back to the CLI automatically
7. Type `/models` and pick a model

### Test

```
Read AGENTS.md and tell me what you see.
```

### Run the setup skill

```
Read 7-Skills/second-brain-setup/SKILL.md and run the workflow described in that file.
```

---

## Path C: OpenCode + a free model

If you do not want to pay for AI at all, run OpenCode against a free model through OpenRouter.

### What is OpenRouter?

A gateway to hundreds of AI models, some of them free. You create an account, get an API key, pick a model.

### Install OpenCode

https://opencode.ai/download

For developers:

```bash
npm i -g opencode-ai
```

### Configure a free model

1. Go to https://openrouter.ai and create an account (free)
2. Generate an API key (Settings -> Keys -> Create Key)
3. Go to the Super Brain folder and launch it:

```bash
cd /path/to/your/super-brain
opencode
```

4. Type `/connect`
5. Pick **OpenRouter** from the list, paste your API key
6. Type `/models` and pick a free model

Free models are slower and less careful than frontier models. They work for ingest; expect to check their output.

### Test

```
Read AGENTS.md and tell me what you see.
```

### Run the setup skill

```
Read 7-Skills/second-brain-setup/SKILL.md and run the workflow described in that file.
```

---

## Path D: Cursor / Windsurf / Antigravity

If you already have an AI-enabled IDE, just open the Super Brain folder as a project. These IDEs read and write files directly, so the Super Brain behaves the same as in the other paths.

1. Open your IDE
2. **File -> Open Folder** (or equivalent) -> pick the Super Brain folder
3. Open the built-in AI chat or agent
4. **Test:**

```
Read AGENTS.md and tell me what you see.
```

5. **Run the setup skill:**

```
Read 7-Skills/second-brain-setup/SKILL.md and run the workflow described in that file.
```

---

## After setup - your first two moves

### 1. Fill in your profile

Run `second-brain-setup` and answer the questions. If you have results from Gallup CliftonStrengths, DISC, MBTI or any similar assessment, paste them in - the AI pulls out the parts that change how it should work with you and drops the rest.

### 2. Start your first project

```
Copy 3-Projects/_template to 3-Projects/[your-project-slug] and walk me
through filling in the brief. Ask me one question at a time.
```

Read `3-Projects/README.md` first if you want to know how the index and the log work.

---

## Something not working?

| Problem | Fix |
|---|---|
| The AI cannot see the files | Check that you opened the FOLDER, not a single file |
| OpenCode: `/connect` does nothing | Make sure you have the latest version from https://opencode.ai/download |
| Obsidian shows no folders | Choose "Open folder as vault", not "Create new vault" |
| The skill does not work as a slash command | Use the ad-hoc method: "Read the SKILL.md and run the workflow" |
| `about.md` is still empty after running the skill | The AI should have written the file. Check in Obsidian. If it is empty, run it again. |
